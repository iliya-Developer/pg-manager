import requests
from datetime import datetime, timezone, timedelta

class PanelClient:
    def __init__(self, address, username, password):
        self.address = address.replace("/dashboard", "").rstrip("/")
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.token = None

    def login(self):
        url = f"{self.address}/api/admin/token"

        data = {
            "grant_type": "password",
            "username": self.username,
            "password": self.password
        }

        response = self.session.post(url, data=data)
        
        try:
            result = response.json()
            if "access_token" in result:
                self.token = result["access_token"]
        except:
            pass

        return response
    
    def create_users(self, username, status, expire, data_limit, group_ids, on_hold_timeout=None, on_hold_expire_duration=None):
        if not self.token:
            return {"success": False, "error": "login first"}

        url = f"{self.address}/api/user"

        now_utc = datetime.now(timezone.utc)

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        payload = {
            "username": username,
            "status": status,
            "expire": str((now_utc + timedelta(days=expire)).astimezone().isoformat()) if expire else None,
            "data_limit": data_limit * 1073741824,
            "group_ids": group_ids,
            "on_hold_timeout": str((now_utc + timedelta(days=on_hold_timeout)).astimezone().isoformat()) if on_hold_timeout else None,
            "on_hold_expire_duration": on_hold_expire_duration * 24 * (60*60) if on_hold_expire_duration else None,
        }

        response = self.session.post(url, json=payload, headers=headers)

        print(response.status_code)

        if response.status_code == 200 or response.status_code == 201:
            return {'success': True, 'result': response.json()}
        else:
            return {"success": False, "error": response.json()}