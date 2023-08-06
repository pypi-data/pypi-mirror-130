import json

import requests


class ResourceClient:
    session = None
    endpoint = None
    access_token = None
    refresh_token = None

    def __init__(self, session, api_url, access_token, refresh_token):
        self.session = session
        self.api_url = api_url
        self.access_token = access_token
        self.refresh_token = refresh_token

    async def generate_url(self, pk=None, page=None, action=None):
        try:
            api_endpoint = "".join([self.api_url, self.endpoint])
            if pk and action:
                return "".join([api_endpoint, str(pk), "/", str(action), "/"])
            if pk:
                return "".join([api_endpoint, str(pk), "/"])
            if page:
                return f"{api_endpoint}?page={page}"
            if action:
                return "".join([api_endpoint, action, "/"])

            return api_endpoint
        except TypeError:
            print("Wystapil problem")

    def __refresh(self, refresh_token):
        try:
            response = requests.post(f"{self.api_url}/auth/jwt/refresh", data=json.dumps({
                "refresh": refresh_token
            }))
            response.raise_for_status()
            data = response.json()
            return data['access']
        except requests.exceptions.HTTPError as e:
            print(e)

    def get_refresh_token(self):
        return self.__refresh(self.refresh_token)