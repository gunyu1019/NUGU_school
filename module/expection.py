import json

from aiohttp import web

forbidden_msg_en = "This API can only be accessed by NUGU play."
forbidden_msg_ko = "이 API는 NUGU Play를 통해서만 접속 할 수 있습니다."
forbidden = web.Response(status=403, reason=forbidden_msg_en,
                         text=f"Forbidden: {forbidden_msg_en}\n접근거부: {forbidden_msg_ko}")


def isconvert(data):
    try:
        json.loads(data)
    except json.decoder.JSONDecodeError:
        return False
    return True


def exception(msg, version):
    return {
        "version": version,
        "resultCode": msg
    }
