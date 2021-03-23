import datetime
import pytz
from rest_framework import status
import json


def success_response(data):
    data = {"status": status.HTTP_200_OK, "success": True, "now_date": getnowDate(), "data": data}
    return data


def error_response(exception):
    data = {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "success": False, "message": exception}
    return data


def deny_response(message):
    data = {"status": status.HTTP_403_FORBIDDEN, "success": False, "message": message}
    return data


def getnowDate():
    tz = pytz.timezone("Asia/Jakarta")
    utc = pytz.timezone("UTC")
    date_tz = utc.localize(datetime.datetime.now())
    local_date = date_tz.astimezone(tz)
    return local_date.strftime("%Y-%m-%d %H:%M:%S")