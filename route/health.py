from aiohttp.web import Response


async def health(request):
    return Response(status=200, text="OK")
