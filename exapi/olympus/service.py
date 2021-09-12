import requests
from utils.error import mk_runtime_error
from http import HTTPStatus
from ide_proxy.config import Config


class OlympusExapi:
    def __init__(self, url: str):
        self._url = url

    def signin_with_token(self, token):
        payload = {
            "data": {
                "token": token,
            },
            "strategy": "google",
        }
        response = requests.post(f"{self._url}/api/users/signin/", json=payload)

        if response.status_code != HTTPStatus.OK:
            raise RuntimeError(mk_runtime_error(response))

        return response.json()["jwt"]

    def verify_token(self, jwt):
        payload = {"jwt": jwt}
        response = requests.post(f"{self._url}/api/sessions/verify/", json=payload)

        if response.status_code not in [HTTPStatus.OK, HTTPStatus.UNAUTHORIZED]:
            raise RuntimeError(mk_runtime_error(response))

        return response.json()["verified"]


def get_olympus_exapi():
    return OlympusExapi(url=Config.OLYMPUS_PROXY_URL)
