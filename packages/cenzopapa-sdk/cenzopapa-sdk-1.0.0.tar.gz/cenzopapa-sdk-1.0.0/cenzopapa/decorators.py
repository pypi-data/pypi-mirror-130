import requests.exceptions


def check_authorization(decorated):
    def wrapper(api, *args, **kwargs):
        try:
            return decorated(api, *args, **kwargs)
        except requests.exceptions.HTTPError as e:
            try:
                response = requests.post(f"{api.api_url}/auth/jwt/refresh", {
                    'refresh': api.refresh_token
                })
                data = response.json()
                api.access_token = data['access']
                return decorated(api, *args, **kwargs)
            except KeyError:
                print("Musisz sie zalogowac")

    return wrapper
