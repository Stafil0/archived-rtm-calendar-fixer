from pytz import timezone


def replace_timezone(dt, zone):
    return dt.replace(tzinfo=timezone(zone))
