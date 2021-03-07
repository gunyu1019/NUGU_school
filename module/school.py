import json
from config import parser
from .request import requests

Type_list = {"초등학교": "els", "중학교": "mis", "고등학교": "his", "특수학교": "sps"}


class school_exception:
    NotFound = 404
    Internal_Server_Error = 501


class school:
    def __init__(self, school_nm):
        self.school_nm = school_nm
        self.token = parser.get('TOKEN', 'token')
        self.base = "https://open.neis.go.kr/hub"

        self.school_data = None

    async def school(self, location: str = None):
        header = {'Type': 'json', 'KEY': f'{self.token}', 'SCHUL_NM': self.school_nm}

        resp = await requests("GET", f"{self.base}/schoolInfo", params=header)
        if isinstance(resp.data, str):
            json1 = json.loads(resp.data)
        else:
            json1 = resp.data

        if 'RESULT' in json1.keys():
            if 'CODE' in json1['RESULT'].keys():
                ercode = json1['RESULT']['CODE']
                if ercode == 'INFO-200':
                    return school_exception.NotFound
                elif ercode.startswith("ERROR") or ercode == 'INFO-300':
                    return school_exception.Internal_Server_Error

        school_data = json1['schoolInfo'][1]["row"]
        result = []

        if location is not None:
            for i in school_data:
                if i.get("ORG_RDNMA").find(location) != -1:
                    result.append(i)
            if len(result) == 0:
                return school_exception.NotFound
        else:
            result = school_data
        self.school_data = result
        return result

    async def meal(self, school_data: dict, **kwargs):
        header = {'Type': 'json', 'KEY': f'{self.token}', 'ATPT_OFCDC_SC_CODE': school_data.get('ATPT_OFCDC_SC_CODE'),
                  'SD_SCHUL_CODE': school_data.get('SD_SCHUL_CODE')}
        header.update(**kwargs)

        resp2 = await requests("GET", f"{self.base}/mealServiceDietInfo", params=header)
        if isinstance(resp2.data, str):
            json2 = json.loads(resp2.data)
        else:
            json2 = resp2.data

        if 'RESULT' in json2.keys():
            if 'CODE' in json2['RESULT'].keys():
                ercode = json2['RESULT']['CODE']
                if ercode == 'INFO-200':
                    return school_exception.NotFound
                elif ercode.startswith("ERROR") or ercode == 'INFO-300':
                    return school_exception.Internal_Server_Error

        return json2

    async def timetable(self, school_data, GRADE, CLASS, **kwargs):
        header = {'Type': 'json', 'KEY': f'{self.token}', 'ATPT_OFCDC_SC_CODE': school_data.get('ATPT_OFCDC_SC_CODE'),
                  'SD_SCHUL_CODE': school_data.get('SD_SCHUL_CODE'), 'GRADE': GRADE.rstrip("학년"),
                  'CLASS_NM': CLASS.rstrip("반")}
        header.update(**kwargs)

        type_nm = school_data.get('SCHUL_KND_SC_NM')
        resp2 = await requests("GET", f"{self.base}/{Type_list[type_nm]}Timetable", params=header)
        if isinstance(resp2.data, str):
            json2 = json.loads(resp2.data)
        else:
            json2 = resp2.data

        if 'RESULT' in json2.keys():
            if 'CODE' in json2['RESULT'].keys():
                ercode = json2['RESULT']['CODE']
                if ercode == 'INFO-200':
                    return school_exception.NotFound
                elif ercode.startswith("ERROR") or ercode == 'INFO-300':
                    return school_exception.Internal_Server_Error

        return json2
