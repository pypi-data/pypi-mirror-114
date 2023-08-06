import hashlib

import aiohttp.web
import requests

# import httptools


class AsyncClientSession(aiohttp.ClientSession):
    """
    Async http session that dereferences it's connection when deleted (Since it is stored elsewhere on the hub)
    """

    def __del__(self):
        if not self.closed:
            self._connector = None


class AsyncConnector(aiohttp.TCPConnector):
    """
    An async connector that cleans up and doesn't spew warnings when it is deleted
    """

    def __del__(self):
        for ev in self._throttle_dns_events.values():
            ev.cancel()
        super()._close()


def __init__(hub):
    hub.tool.http.session.COOKIES = aiohttp.CookieJar(unsafe=False, quote_cookie=True)
    hub.tool.http.session.APP = aiohttp.web.Application()


def __func_alias__(hub):
    """
    pop construct to put request methods on the hub
    """

    def _get_caller(method):
        async def _request(ctx, url: str, **kwargs):
            return await hub.tool.http.session.request(ctx, method, url=url, **kwargs)

        return _request

    return {
        method: _get_caller(method)
        for method in ("delete", "head", "get", "patch", "post", "put")
    }


async def request(hub, ctx, method: str, url: str, **kwargs) -> aiohttp.ClientResponse:
    """
    Make an aiohttp request using the named method
    :param hub:
    :param ctx: The context retrieved from the acct plugin
    :param method: delete|get|head|patch|post|put
    :param url: The url to request
    :param kwargs: kwargs to pass directly to aiohttp.ClientSession.request
    :return: A requests-like response
    """
    session = await hub.tool.http.session.client(ctx)
    return await session.request(method=method, url=url, **kwargs)


def _generate_key(**kwargs) -> str:
    """
    Generate a unique but reproducible key from a dictionary
    """
    return hashlib.sha512(
        b"".join((str(k) + str(kwargs[k])).encode() for k in sorted(kwargs.keys()))
    ).hexdigest()


async def client(hub, ctx, client_class=AsyncClientSession) -> aiohttp.ClientSession:
    """
    Create an aiohttp Client Session based on the context
    """
    session_kwargs = ctx.acct.get("session", {})
    auth = ctx.acct.get("Auth")

    hub.acct.UNLOCKED = True

    client_key = "client_" + _generate_key(auth=auth, **session_kwargs)
    if client_key not in hub.tool.http.session.APP:
        hub.tool.http.session.APP[client_key] = client_class(
            auth=auth,
            connector=await hub.tool.http.session.connector(ctx),
            headers=ctx.acct.get("headers", {}),
            cookie_jar=hub.tool.http.session.COOKIES,
            **session_kwargs,
        )
    return hub.tool.http.session.APP[client_key]


async def resolver(
    hub, ctx, resolver_class=aiohttp.AsyncResolver
) -> aiohttp.AsyncResolver:
    """
    Retrieve the resolver for the given context, create it if it doesn't exist
    """
    resolver_kwargs = ctx.acct.get("resolver", {})

    resolver_key = "resolver_" + _generate_key(**resolver_kwargs)
    if resolver_key not in hub.tool.http.session.APP:
        hub.tool.http.session.APP[resolver_key] = resolver_class(**resolver_kwargs)
    return hub.tool.http.session.APP[resolver_key]


async def connector(hub, ctx, connector_class=AsyncConnector) -> aiohttp.BaseConnector:
    """
    Retrieve the connector for the given context, create it if it doesn't exist
    """
    resolve = await hub.tool.http.session.resolver(ctx)
    connector_kwargs = ctx.acct.get("connector", {})
    connector_key = "connector_" + _generate_key(resolve=resolve, **connector_kwargs)
    if connector_key not in hub.tool.http.session.APP:
        hub.tool.http.session.APP[connector_key] = connector_class(
            resolver=resolve,
            **connector_kwargs,
        )

    return hub.tool.http.session.APP[connector_key]
