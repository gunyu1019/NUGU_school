from datetime import datetime
from aiohttp.web import json_response

from module.expection import forbidden, isconvert, exception
from module.date import date, getWeekLastDate, getWeekFirstDate, change_weekday
from module.school import school, school_exception
from config import parser


def read_food(food):
    food_list = food.split('<br/>')
    answer = ", ".join(food_list)
    for i in range(18, 0, -1):
        answer = answer.replace(f"{i}.", "")
    return answer.replace("+", "")


def read_food_display(food):
    food_list = food.split('<br/>')
    answer = ", ".join(food_list)
    return answer.replace("+", "")


async def meal(request):
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

    school_nm = parameters.get('MEAL_SCHOOL_NM').get('value')
    sc_m = school(school_nm)

    if 'MEAL_LCP' in parameters:
        location = parameters.get('MEAL_LCP').get('value')
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

    if "MEAL_DT_2" in parameters:
        dateV = date(
            parameters.get("MEAL_DT_1"),
            parameters.get("MEAL_DT_2")
        )
    else:
        dateV = date(parameters.get("MEAL_DT_1"))

    if dateV is None:
        return json_response(
            exception("date_not_found", version),
            status=200)
    json_data = await sc_m.meal(
        data[0],
        MLSV_YMD=dateV.datetime.strftime('%Y%m%d'))

    listItems = []
    if display:
        date_inform = {}
        firstDay = getWeekFirstDate(dateV.datetime).strftime('%Y%m%d')
        lastDay = getWeekLastDate(dateV.datetime).strftime('%Y%m%d')
        for i in range(int(firstDay), int(lastDay)):
            if str(i) == dateV.datetime.strftime('%Y%m%d'):
                continue
            date_inform[str(i)] = None

        dp_json_data = await sc_m.meal(
            data[0],
            MLSV_FROM_YMD=firstDay,
            MLSV_TO_YMD=lastDay)
        mt = parameters.get('MEAL_TYPE').get('value')

        food = None
        for i in json_data.get('mealServiceDietInfo')[1].get("row"):
            if i['MMEAL_SC_NM'] == parameters.get('MEAL_TYPE').get('value'):
                food = i.get("DDISH_NM")

        if food is not None:
            listItems.append({
                "token": display_token,
                "header": {
                    "text": f"{change_weekday(dateV.datetime.weekday())} {mt}"
                },
                "body": [{
                    "text": f"{read_food_display(food)}"
                }]
            })
        else:
            listItems.append({
                "token": display_token,
                "header": {
                    "text": f"{change_weekday(dateV.datetime.weekday())} {mt}"
                },
                "body": [{
                    "text": "급식정보 없음."
                }],
                "footer": {
                    "text": "휴교 중이거나, 방학 중에는 급식 정보가 없습니다."
                }
            })

        for i in dp_json_data.get('mealServiceDietInfo')[1].get("row"):
            if i.get('MMEAL_SC_NM') == parameters.get('MEAL_TYPE').get('value'):
                if i.get("MLSV_YMD") not in date_inform:
                    continue
                date_inform[i.get("MLSV_YMD")] = i

        for i in range(int(firstDay), int(lastDay)):
            if str(i) == dateV.datetime.strftime('%Y%m%d'):
                continue

            date_time_obj = datetime.strptime(str(i), '%Y%m%d')
            if date_inform[str(i)] is None:
                listItems.append({
                    "token": display_token,
                    "header": {
                        "text": f"{change_weekday(date_time_obj.weekday())} {mt}"
                    },
                    "body": [{
                        "text": "급식정보 없음."
                    }],
                    "footer": {
                        "text": "휴교 중이거나, 방학 중에는 급식 정보가 없습니다."
                    }
                })
                continue
            cacheDT = date_inform[str(i)]
            listItems.append({
                "token": display_token,
                "header": {
                    "text": f"{change_weekday(date_time_obj.weekday())} {mt}"
                },
                "body": [{
                    "text": f"{read_food_display(cacheDT.get('DDISH_NM'))}"
                }]
            })

    if json_data is school_exception.NotFound:
        return json_response(
            exception("meal_not_found1", version),
            status=200)
    elif json_data is school_exception.Internal_Server_Error:
        return json_response(
            exception("backend_proxy_error", version),
            status=200)

    food = None
    for i in json_data.get('mealServiceDietInfo')[1].get("row"):
        if i['MMEAL_SC_NM'] == parameters.get('MEAL_TYPE').get('value'):
            food = i.get("DDISH_NM")

    if food is None:
        return json_response(
            exception("meal_not_found2", version),
            status=200)

    data = {
        "version": version,
        "resultCode": "OK",
        "output": {
            "DT_ANSWER": dateV.name,
            "MEAL_STATUS": read_food(food)
        }
    }
#   Capability Interface 처리
    if display:
        data['directives'] = [{
            "type": "Display.TextList3",
            "version": display_version,
            "playServiceId": playServiceId,
            "token": display_token,
            "title": {
                "logo": {
                    "sources": [
                        {
                            "url": "http://someurl.com/name.png"
                        }
                    ]
                },
                "text": {
                    "text": f"{SCHUL_NM}의 급식 정보"
                }
            },
            "badgeNumber": "False",
            "listItems": listItems,
            "caption": "알레르기 정보: 1.난류, 2.우유, 3.메밀, 4.땅콩, 5.대두, 6.밀, 7.고등어, 8.게, 9.새우, 10.돼지고기, 11.복숭아, 12.토마토, 13.아황산염, 14.호두, 15.닭고기, 16.쇠고기, 17.오징어, 18.조개류(굴,전복,홍합 등)"
        }]

    return json_response(data, status=200)
