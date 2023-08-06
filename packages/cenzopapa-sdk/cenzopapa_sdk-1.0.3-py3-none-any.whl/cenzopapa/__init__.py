from cenzopapa.resources import ImageResource, JWTResource

__version__ = "1.0.3"


class Cenzopapa:

    def __init__(self, api_url=None):
        if not api_url:
            self.api_url = "https://api.jebzpapy.tk"
        self.api_url = api_url
        self.access_token = None
        self.refresh_token = None

        self.image = ImageResource(api_url=api_url, access_token=self.access_token, refresh_token=self.refresh_token)
