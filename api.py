from fastapi import APIRouter
from panel_client import PanelClient

router = APIRouter()

@router.get("/")
def root():
    return {"message": "Api is running"}

@router.post("/create-users")
def create_users(body: dict):
    address = body.get("address")
    panel_username = body.get("panel_username")
    panel_password = body.get("panel_password")
    username = body.get("username")
    status = body.get("status")
    expire = body.get("expire")
    data_limit = body.get("data_limit")
    group_ids = body.get("group_ids")
    on_hold_timeout = body.get("on_hold_timeout")
    on_hold_expire_duration = body.get("on_hold_expire_duration")

    client = PanelClient(address, panel_username, panel_password)
    login_response = client.login()
    if not client.token:
        try:
            return {"success": False, "error": login_response.json()}
        except:
            return {"success": False, "raw": login_response.text}
    response = client.create_users(username, status, expire, data_limit, group_ids, on_hold_timeout, on_hold_expire_duration)

    if response.get("success") == True:
        return {"success": True, "message": "users created successfully"}
    else:
        return response