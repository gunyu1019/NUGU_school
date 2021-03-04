import datetime

from module.model import datetime as dm


def response(dd, dn):
    return dm({
        "name": dn,
        "datetime": dd
    })


def add_days(sourceDate, count):
    targetDate = sourceDate + datetime.timedelta(days=count)
    return targetDate


def getWeekFirstDate(sourceDate):
    temporaryDate = datetime.datetime(sourceDate.year, sourceDate.month, sourceDate.day)
    weekDayCount = temporaryDate.weekday()
    targetDate = add_days(temporaryDate, -weekDayCount)
    return targetDate


def getWeekLastDate(sourceDate):
    temporaryDate = getWeekFirstDate(sourceDate)
    targetDate = add_days(temporaryDate, 5)
    return targetDate


def date(param1=None, param2=None):
    if param2 is None:
        param2 = {"type": "NoneType", "value": None}
    if param1 is None:
        param1 = {"type": "NoneType", "value": None}

    now = datetime.datetime.now()
    if param1.get("value") == "TODAY" and param2 is {"type": "NoneType", "value": None}:
        return response(now, "오늘")

    if param1.get("type") == "BID_DT_DAY":
        if "TODAY" == param1.get("value"):
            return response(now, "오늘")
        elif "TOMORROW" == param1.get("value"):
            return response(add_days(now, 1), "내일")
        elif "A_TOMORROW" == param1.get("value"):
            return response(add_days(now, 2), "내일모레")
        elif "AA_TOMORROW" == param1.get("value"):
            return response(add_days(now, 3), "글피")
        elif "AAA_TOMORROW" == param1.get("value"):
            return response(add_days(now, 4), "그글피")
        elif "YESTERDAY" == param1.get("value"):
            return response(add_days(now, -1), "어제")
        elif "B_YESTERDAY" == param1.get("value"):
            return response(add_days(now, -2), "그저께")
        elif "BB_YESTERDAY" == param1.get("value"):
            return response(add_days(now, -3), "그그저께")
        else:
            return None
    elif param1.get("type") == "BID_DT_MDAY":
        if param2.get("type") == "BID_DT_YMONTH":
            month = param2.get('value')
        else:
            month = now.month
        day = param1.get('value')
        try:
            dt = datetime.datetime(now.year, int(month), int(day))
        except ValueError:
            return None
        return response(dt, f"{month}월 {day}일")
    elif param1.get("type") == "BID_DT_WDAY":
        firstDay = getWeekFirstDate(now)

        param2Type = False
        if param1.get("value").startswith("SUN"):
            param2Type = True
            if param1.get("value") == "SUN.W.-1":
                weekDay = add_days(firstDay, -1)
                weekAnswer = "지난주 일요일"
            elif param1.get("value") == "SUN.W.-2":
                weekDay = add_days(firstDay, -8)
                weekAnswer = "지지난주 일요일"
            elif param1.get("value") == "SUN.W.1":
                weekDay = add_days(firstDay, 13)
                weekAnswer = "다음주 일요일"
            elif param1.get("value") == "SUN.W.2":
                weekDay = add_days(firstDay, 20)
                weekAnswer = "다다음주 일요일"
            else:
                weekDay = add_days(firstDay, 6)
                weekAnswer = "일요일"
        elif param1.get("value").startswith("WEEKBEGIN"):
            param2Type = True
            if param1.get("value") == "WEEKBEGIN.W.-1":
                weekDay = add_days(firstDay, -7)
                weekAnswer = "지난주 월요일"
            elif param1.get("value") == "WEEKBEGIN.W.-2":
                weekDay = add_days(firstDay, -14)
                weekAnswer = "지지난주 월요일"
            elif param1.get("value") == "WEEKBEGIN.W.1":
                weekDay = add_days(firstDay, 7)
                weekAnswer = "다음주 월요일"
            elif param1.get("value") == "WEEKBEGIN.W.2":
                weekDay = add_days(firstDay, 14)
                weekAnswer = "다다음주 월요일"
            else:
                weekDay = firstDay
                weekAnswer = "월요일"
        elif param1.get("value") == "MON":
            weekDay = firstDay
            weekAnswer = "월요일"
        elif param1.get("value") == "TUE":
            weekDay = add_days(firstDay, 1)
            weekAnswer = "화요일"
        elif param1.get("value") == "WED":
            weekDay = add_days(firstDay, 2)
            weekAnswer = "수요일"
        elif param1.get("value") == "THU":
            weekDay = add_days(firstDay, 3)
            weekAnswer = "목요일"
        elif param1.get("value") == "FRI":
            weekDay = add_days(firstDay, 4)
            weekAnswer = "금요일"
        elif param1.get("value") == "SAT":
            weekDay = add_days(firstDay, 5)
            weekAnswer = "토요일"
        else:
            return None

        if param2.get("type") == "BID_DT_WEEK" and not param2Type:
            week = param2.get('value')
            if week == "W.0":
                weekAnswer = "이번주 " + weekAnswer
            elif week == "W.1":
                weekAnswer = "다음주 " + weekAnswer
                weekDay = add_days(weekDay, 7)
            elif week == "W.2":
                weekAnswer = "다다음주 " + weekAnswer
                weekDay = add_days(weekDay, 14)
            elif week == "W.3":
                weekAnswer = "다다다음주 " + weekAnswer
                weekDay = add_days(weekDay, 21)
            elif week == "W.-1":
                weekAnswer = "지난주 " + weekAnswer
                weekDay = add_days(weekDay, -7)
            elif week == "W.-2":
                weekAnswer = "지지난주 " + weekAnswer
                weekDay = add_days(weekDay, -14)
            elif week == "W.-3":
                weekAnswer = "지지난주 " + weekAnswer
                weekDay = add_days(weekDay, -21)

        return response(weekDay, weekAnswer)
    elif param2.get("type") == "BID_DT_WEEK":
        week = param2.get('value')
        if week == "W.0":
            return response(now, "이번주")
        elif week == "W.1":
            return response(add_days(now, 7), "다음주")
        elif week == "W.2":
            return response(add_days(now, 14), "다다음주")
        elif week == "W.3":
            return response(add_days(now, 21), "다다다음주")
        elif week == "W.-1":
            return response(add_days(now, -7), "지난주")
        elif week == "W.-2":
            return response(add_days(now, -14), "지지난주")
        elif week == "W.-3":
            return response(add_days(now, -21), "지지지난주")


def change_weekday(weekday):
    weekday_data = {
        0: "월요일",
        1: "화요일",
        2: "수요일",
        3: "목요일",
        4: "금요일",
        5: "토요일",
        6: "일요일"
    }
    return weekday_data[weekday]