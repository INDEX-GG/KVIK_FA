import requests
from app.core.config import settings

auth_url = "https://pbx-guru-2.web.pbxmaker.ru/index.php/restapi/auth"
call_url = "https://pbx-guru-2.web.pbxmaker.ru/index.php/restapi/number/call-auth"
approve_url = "https://pbx-guru-2.web.pbxmaker.ru/index.php/restapi/number/approve"


def auth():
    try:
        data = {
            "grant_type": "password",
            "scope": "number",
            "client_id": settings.PHONE_LOGIN,
            "client_secret": settings.PHONE_PASSWORD}
        response = requests.post(auth_url, data=data)
        access_token = response.json()["access_token"]
        return access_token
    except Exception:
        return False


def call(access_token, phone_num):
    try:
        data = {"caller_id": str(phone_num)}
        headers = {"Authorization": "Bearer {}".format(access_token)}
        response = requests.post(call_url, data=data, headers=headers)
        caller_id = response.json()["caller_id"]
        tmp_caller_id = response.json()["tmp_caller_id"]
        return {"caller_id": caller_id, "tmp_caller_id": tmp_caller_id}
    except Exception:
        return False


def approve(access_token, caller_id, tmp_caller_id):
    try:
        data = {
            "action": "call-auth",
            "caller_id": caller_id,
            "tmp_caller_id": tmp_caller_id
        }
        headers = {"Authorization": "Bearer {}".format(access_token)}
        response = requests.post(approve_url, data=data, headers=headers)
        return response.json()
    except Exception:
        return False


def call_to_phone(phone_num):
    try:
        access_token = auth()
        make_call = call(access_token=access_token, phone_num=phone_num)
        caller_id = make_call["caller_id"]
        tmp_caller_id = make_call["tmp_caller_id"]
        call_approve = approve(access_token=access_token, caller_id=caller_id, tmp_caller_id=tmp_caller_id)
        if call_approve["success"] is True:
            return tmp_caller_id[-4:]
        else:
            return False
    except Exception:
        return False
