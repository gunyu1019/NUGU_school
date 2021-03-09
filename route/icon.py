from aiohttp.web import FileResponse


async def icon(request):
    return FileResponse('file/icon.png')
