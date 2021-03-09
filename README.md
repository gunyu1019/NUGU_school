# NUGUplay "학교알리미"
SKT 인공지능 플랫폼, NUGU를 통하여 학교 정보를 알 수 있는 NUGU PLAY입니다.
기존 [레포](https://github.com/gunyu1019/NUGU_school_old) 는 Sanic으로 제작된 반면, 이번에는 aiohttp 서버를 활용하여 제작해보았습니다.

* NUGUplay에서 제공하는 Backend는 오직 "NUGU" 사용자를 위한 것으로 실제 타 사용자는 해당 백엔드에 접근하실 수 없습니다.
* 모든 API는 `https://yhs.kr/api/NUGU/` 로 구성되어 있습니다.
* 해당 API는 시간에 대한 문제는 크게 없지만, 날짜는 UTC+9(한국시간)으로 계산합니다.
* 응답형식은 접근 거부(403), Method 비허가(405)를 제외한 모두 `json/application`의 형태로 반환됩니다.
* 모든 값은 Body(json)형태로 보내야 합니다.
* `Request Body`와 `Response`는 단지, 예시일분 실제로는 일부 값이 변경되어 반환될 수 있습니다.

### 종류
NUGU Backend에서는 2가지의 API를 지원합니다.

#### /meal
```
https://yhs.kr/api/NUGU/meal
```
본 기능은 급식 정보에 대한 백엔드 입니다.

* Request Body
```json
{
    "version": "1.0",
    "action": {
        "actionName": "meal",
        "parameters": {
            "MEAL_DT_1": {
                "type": "BID_DT_DAY",
                "value": "{{BID_DT 형태의 DATE}}"
            },
            "MEAL_SCHOOL_NM": {
                "type": "SCHOOL_NAME",
                "value": "{{School Name}}"
            },
            "MEAL_TYPE": {
                "type": "MEAL_TYPE",
                "value": "{{MEAL_TYPE 형태의 아침, 점심 저녁 값 | default : 중식}}"
            },
            "KEY": {
                "value": "{{Backend Access Key Value}}"
            }
        }
    },
    "context": {
        "session": {
            "isPlayBuilderRequest": "True",
            "id": "{{session id}}",
            "isNew": "True"
        },
        "supportedInterfaces": {
            "Display": {
                "version": "1.0",
                "token": "{{Display token}}",
                "playServiceId": "{{playServiceId}}"
            }
        },
        "device": {
            "type": "speaker",
            "state": {}
        }
    }
}
```
* Response
```json
{
    "version": "1.0",
    "resultCode": "OK",
    "output": {
        "DT_ANSWER": "{{DT_ANSWER Data}}",
        "MEAL_STATUS": "{{Meal Data}}"
    },
    "directives": [
        {
            "type": "Display.TextList3",
            "version": "1.0",
            "playServiceId": "{{playServiceId}}",
            "token": "{{Display token}}",
            "title": {
                "logo": {
                    "sources": [
                        {
                            "url": "{{Source Image}}"
                        }
                    ]
                },
                "text": {
                    "text": "{{School Name}}의 급식 정보"
                }
            },
            "badgeNumber": "False",
            "listItems": [
                {
                    "token": "{{Display token}}",
                    "header": {
                        "text": "목요일 중식"
                    },
                    "body": [
                        {
                            "text": "{{Meal Data}}"
                        }
                    ]
                },
                {
                    "token": "{{Display token}}",
                    "header": {
                        "text": "월요일 중식"
                    },
                    "body": [
                        {
                            "text": "{{Meal Data}}"
                        }
                    ]
                },
                {
                    "token": "{{Display token}}",
                    "header": {
                        "text": "화요일 중식"
                    },
                    "body": [
                        {
                            "text": "{{Meal Data}}"
                        }
                    ]
                },
                {
                    "token": "{{Display token}}",
                    "header": {
                        "text": "수요일 중식"
                    },
                    "body": [
                        {
                            "text": "{{Meal Data}}"
                        }
                    ]
                },
                {
                    "token": "{{Display token}}",
                    "header": {
                        "text": "금요일 중식"
                    },
                    "body": [
                        {
                            "text": "{{Meal Data}}"
                        }
                    ]
                }
            ],
            "caption": "알레르기 정보: 1.난류, 2.우유, 3.메밀, 4.땅콩, 5.대두, 6.밀, 7.고등어, 8.게, 9.새우, 10.돼지고기, 11.복숭아, 12.토마토, 13.아황산염, 14.호두, 15.닭고기, 16.쇠고기, 17.오징어, 18.조개류(굴,전복,홍합 등)"
        }
    ]
}
```
#### /timetable
```
https://yhs.kr/api/NUGU/timetable
```
본 기능은 시간표 정보에 대한 백엔드 입니다.

* Request Body
```json
{
    "version": "1.0",
    "action": {
        "actionName": "timetable",
        "parameters": {
            "TIMETABLE_DT_1": {
                "type": "BID_DT_DAY",
                "value": "{{BID_DT 형태의 DATE}}"
            },
            "TIMETABLE_SCHOOL_NM": {
                "type": "SCHOOL_NAME",
                "value": "{{School Name}}"
            },
            "TIMETABLE_CLASS": {
                "type": "CLASS",
                "value": "{{Class | n반}}"
            },
            "TIMETABLE_GRADE": {
                "type": "GRADE",
                "value": "{{Grade | n학년}}"
            },
            "KEY": {
                "value": "{{Backend Access Key Value}}"
            }
        }
    },
    "context": {
        "session": {
            "isPlayBuilderRequest": "True",
            "id": "{{session id}}",
            "isNew": "True"
        },
        "supportedInterfaces": {
            "Display": {
                "version": "1.0",
                "token": "{{Display token}}",
                "playServiceId": "{{playServiceId}}"
            }
        },
        "device": {
            "type": "speaker",
            "state": {}
        }
    }
}
```
* Response
```json
{
    "version": "1.0",
    "resultCode": "OK",
    "output": {
        "TIMETABLE_STATUS": "{{TIMETABLE_STATUS DATA | 1교시. 국어, 2교시. 수학 ... }}",
        "DT_ANSWER": "{{DT_ANSWER DATA}}"
    },
    "directives": [
        {
            "type": "Display.TextList1",
            "version": "1.0",
            "playServiceId": "{{playServiceId}}",
            "token": "{{Display token}}",
            "title": {
                "logo": {
                    "sources": [
                        {
                            "url": "https://yhs.kr/api/NUGU/icon"
                        }
                    ]
                },
                "text": {
                    "text": "{{School Name}} {{GRADE}} {{CLASS}}의 시간표 정보"
                }
            },
            "badgeNumber": "False",
            "listItems": [
                {
                    "token": "{{Display token}}",
                    "header": {
                        "text": "1 교시"
                    },
                    "body": {
                        "text": "국어"
                    }
                }
            ]
        }
    ]
}
```