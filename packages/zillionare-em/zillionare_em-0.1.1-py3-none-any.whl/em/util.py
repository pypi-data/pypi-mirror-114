import arrow


def date_as_filename():
    dt = arrow.now().date()
    return f"{dt.year:02d}-{dt.month:02d}-{dt.day:02d}"


def datetime_as_filename(timezone: str = "Asia/Shanghai"):
    dt = arrow.now(timezone).datetime
    return f"{date_as_filename()}_{dt.hour:02d}-{dt.minute:02d}-{dt.second:02d}"
