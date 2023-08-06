import requests

from cenzopapa.resources import ImageResource, JWTResource


class Cenzopapa:

    def __init__(self, api_url=None):
        if not api_url:
            self.api_url = "https://api.jebzpapy.tk"
        self.api_url = api_url
        self.session = requests.Session()
        self.access_token = None
        self.refresh_token = None

        self.image = ImageResource(session=self.session, api_url=api_url, access_token=self.access_token, refresh_token=self.refresh_token)
        self.jwt = JWTResource(session=self.session, api_url=api_url, access_token=self.access_token, refresh_token=self.refresh_token)

    def login(self, username, password):
        try:
            response = self.jwt.create({
                "username": username,
                "password": password
            })
            response.raise_for_status()
            data = response.json()
            self.access_token = data['access']
            self.refresh_token = data['refresh']
            self.session.headers.update({
                'Authorization': f'Bearer {self.access_token}'
            })
            self.image.session = self.session
            self.image.access_token = self.access_token
            self.image.refresh_token = self.refresh_token
            self.jwt.session = self.session
            self.jwt.access_token = self.access_token
            self.jwt.refresh_token = self.refresh_token
        except requests.exceptions.HTTPError as e:
            print(e)
