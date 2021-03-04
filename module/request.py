import aiohttp

from module.model import request_model


async def check_content(resp):
    if resp.content_type.startswith("application/json"):
        return await resp.json()
    elif resp.content_type.startswith("image/png"):
        return await resp.content.read()
    elif resp.content_type.startswith("text/html"):
        return await resp.text()
    else:
        None


async def requests(method: str, url: str, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url, **kwargs) as resp:
            data = await check_content(resp)
            request_data = {
                "status": resp.status,
                "data": data,
                "version": resp.version,
                "content-type": resp.content_type,
                "reason": resp.reason
            }
            return request_model(request_data)
