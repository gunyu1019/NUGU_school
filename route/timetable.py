from aiohttp.web import json_response

from module.expection import forbidden, isconvert, exception
from module.date import date
from module.school import school, school_exception, Type_list
from config import parser


async def timetable(request):
    if not request.body_exists or not isconvert(await request.text()):
        return forbidden
    parameters = await request.json()
    action = parameters.get('action')
    version = parameters.get('version')
    context = parameters.get('context')

    if "parameters" in action or action is not None:
        parameters = action.get('parameters')
        if parameters.get('KEY').get('value') != parser.get('TOKEN', 'key'):
            return forbidden
    else:
        return forbidden

    display = False
    if context is not None:
        interface = context.get("supportedInterfaces")
        if "Display" in interface:
            display = True
            display_version = interface.get("Display").get("version")
            display_token = interface.get("Display").get("token")
            playServiceId = interface.get("Display").get("playServiceId")

    school_nm = parameters.get('TIMETABLE_SCHOOL_NM').get('value')
    sc_m = school(school_nm)

    if 'TIMETABLE_LCP' in parameters:
        location = parameters.get('TIMETABLE_LCP').get('value')
        data = await sc_m.school(location)
    else:
        data = await sc_m.school()

    if data is school_exception.NotFound:
        return json_response(
            exception("school_not_found", version),
            status=200)
    elif data is school_exception.Internal_Server_Error:
        return json_response(
            exception("backend_proxy_error", version),
            status=200)

    if len(data) > 1:
        location_data = []
        for i in data:
            for j in data:
                if i == j:
                    continue
                # 분교 판정 오류를 구분하기 위하여 끝부분이 동일해야함. 또한, 가나다초등학교와 나다초등학교 이런 방식의 명칭을 구분하기 위하여 최소 2자 이상이어야함.
                elif i['SCHUL_NM'].endswith(j['SCHUL_NM']) and i not in location_data and len(i['SCHUL_NM'].replace(j['SCHUL_NM'], "")) > 1:
                    location_data.append(i)

        locate = {}
        for i in location_data:
            # 0번째, 도/시 | 1번째, 시/군/구
            location_i = i.get('ORG_RDNMA').split()
            if location_i[0] not in locate:
                locate[location_i[0]] = list()
            if location_i[1] not in locate[location_i[0]]:
                locate[location_i[0]].append(location_i[1])

        if len(locate) > 1:
            json_data = exception("regional_redundancy_error", version)
            area_candidate = str()
            for i in locate.keys():
                area_candidate += f", {i} {', '.join(locate.get(i))}"

            json_data['output'] = {
                "area_candidate": area_candidate.replace(",", "", 1)
            }
            return json_response(json_data, status=200)
    SCHUL_NM = data[0]['SCHUL_NM']

    if "TIMETABLE_DT_2" in parameters:
        dateV = date(
            parameters.get("TIMETABLE_DT_1"),
            parameters.get("TIMETABLE_DT_2")
        )
    else:
        dateV = date(parameters.get("TIMETABLE_DT_1"))

    if dateV is None:
        return json_response(
            exception("date_not_found", version),
            status=200)
    json_data = await sc_m.timetable(
        data[0],
        ALL_TI_YMD=dateV.datetime.strftime('%Y%m%d'),
        CLASS=parameters.get("TIMETABLE_CLASS").get("value").rstrip("반"),
        GRADE=parameters.get("TIMETABLE_GRADE").get("value").rstrip("학년")
    )

    if json_data is school_exception.NotFound:
        return json_response(
            exception("timetable_not_found", version),
            status=200)
    elif json_data is school_exception.Internal_Server_Error:
        return json_response(
            exception("backend_proxy_error", version),
            status=200)

    type_nm = data[0].get("SCHUL_KND_SC_NM")
    data2 = json_data[f'{Type_list[type_nm]}Timetable'][1]['row']
    data_count = len(data2)
    table = ["" for _ in range(data_count)]

    for i in data2:
        perio = int(i.get('PERIO')) - 1
        table[perio] = i.get('ITRT_CNTNT')

    answer = ""
    count = 1
    for i in table:
        answer += f", {count}교시 {i}"
        count += 1

    data = {
        "version": version,
        "resultCode": "OK",
        "output": {
            "TIMETABLE_STATUS": answer.replace(",", "", 1),
            "DT_ANSWER": dateV.name
        }
    }
#   Capability Interface 처리
    if display:
        count = 1
        listItems = []
        for i in table:
            listItems.append({
                "token": display_token,
                "header": {
                    "text": f"{count} 교시"
                },
                "body": {
                    "text": f"{i}"
                }
            })
            count += 1

        data['directives'] = [{
            "type": "Display.TextList1",
            "version": display_version,
            "playServiceId": playServiceId,
            "token": display_token,
            "title": {
                "logo": {
                    "sources": [
                        {
                            "url": "https://yhs.kr/api/nugu/icon"
                        }
                    ]
                },
                "text": {
                    "text": f"{SCHUL_NM} {parameters.get('TIMETABLE_CLASS').get('value')} {parameters.get('TIMETABLE_CLASS').get('value')}의 시간표 정보"
                }
            },
            "badgeNumber": "false",
            "listItems": listItems,
        }]

    return json_response(data, status=200)
