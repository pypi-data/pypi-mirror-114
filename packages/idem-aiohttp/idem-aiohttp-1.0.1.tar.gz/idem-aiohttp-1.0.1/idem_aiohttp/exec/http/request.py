import aiohttp


async def delete(hub, ctx, url: str, **kwargs):
    async with await hub.tool.http.session.delete(ctx, url=url, **kwargs) as response:
        return {
            "ret": await response.read(),
            "status": response.status == 200,
            "comment": response.reason,
        }


async def get(hub, ctx, url: str, **kwargs):
    async with await hub.tool.http.session.get(ctx, url=url, **kwargs) as response:
        return {
            "ret": await response.read(),
            "status": response.status == 200,
            "comment": response.reason,
        }


async def patch(hub, ctx, url: str, **kwargs):
    async with await hub.tool.http.session.patch(ctx, url=url, **kwargs) as response:
        return {
            "ret": await response.read(),
            "status": response.status == 200,
            "comment": response.reason,
        }


async def post(hub, ctx, url: str, **kwargs):
    async with await hub.tool.http.session.post(ctx, url=url, **kwargs) as response:
        return {
            "ret": await response.read(),
            "status": response.status == 200,
            "comment": response.reason,
        }


async def put(hub, ctx, url: str, **kwargs):
    async with await hub.tool.http.session.put(ctx, url=url, **kwargs) as response:
        return {
            "ret": await response.read(),
            "status": response.status == 200,
            "comment": response.reason,
        }
