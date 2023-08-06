from typing import Dict

import aiohttp
from dict_tools.data import NamespaceDict


async def delete(hub, ctx, url: str, headers: Dict[str, str] = None, **kwargs):
    if not headers:
        headers = {}

    headers["content-type"] = "application/json"
    async with await hub.tool.http.session.delete(
        ctx, url=url, headers=headers, **kwargs
    ) as response:
        return {
            "ret": NamespaceDict(await response.json()),
            "status": response.status == 200,
            "comment": response.reason,
        }


async def get(hub, ctx, url: str, headers: Dict[str, str] = None, **kwargs):
    if not headers:
        headers = {}
    headers["content-type"] = "application/json"

    async with await hub.tool.http.session.get(
        ctx, url=url, headers=headers, **kwargs
    ) as response:
        return {
            "ret": NamespaceDict(await response.json()),
            "status": response.status == 200,
            "comment": response.reason,
        }


async def head(hub, ctx, url: str, headers: Dict[str, str] = None, **kwargs):
    if not headers:
        headers = {}

    headers["content-type"] = "application/json"
    async with await hub.tool.http.session.head(
        ctx, url=url, headers=headers, **kwargs
    ) as response:
        return {
            "ret": NamespaceDict(response.headers),
            "status": response.status == 200,
            "comment": response.reason,
        }


async def patch(hub, ctx, url: str, headers: Dict[str, str] = None, **kwargs):
    if not headers:
        headers = {}

    headers["content-type"] = "application/json"
    async with await hub.tool.http.session.patch(
        ctx, url=url, headers=headers, **kwargs
    ) as response:
        return {
            "ret": NamespaceDict(await response.json()),
            "status": response.status == 200,
            "comment": response.reason,
        }


async def post(hub, ctx, url: str, headers: Dict[str, str] = None, **kwargs):
    if not headers:
        headers = {}

    headers["content-type"] = "application/json"
    async with await hub.tool.http.session.post(
        ctx, url=url, headers=headers, **kwargs
    ) as response:
        return {
            "ret": NamespaceDict(await response.json()),
            "status": response.status == 200,
            "comment": response.reason,
        }


async def put(hub, ctx, url: str, headers: Dict[str, str] = None, **kwargs):
    if not headers:
        headers = {}

    headers["content-type"] = "application/json"
    async with await hub.tool.http.session.put(
        ctx, url=url, headers=headers, **kwargs
    ) as response:
        return {
            "ret": NamespaceDict(await response.json()),
            "status": response.status == 200,
            "comment": response.reason,
        }
