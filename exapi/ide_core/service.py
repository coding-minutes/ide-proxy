import requests
from http import HTTPStatus

from utils.requests import ExRequestSession
from exapi.ide_core.models import CodeFile
from utils.make_error import runtime_error
from ide_proxy.config import Config


class IdeCoreExApi:
    def __init__(self, url: str):
        self._url = url
        self._session = ExRequestSession()

    def get_code(self, code_id: int):
        response = self._session.get(f"{self._url}/codes/{code_id}")

        if response.status_code != HTTPStatus.OK:
            raise RuntimeError(runtime_error(response))

        data = response.json()

        return CodeFile.from_dict(dikt=data)

    def save_code(self, source: str, user_email: str, lang: str, input: str):
        body = {
            "source": source,
            "lang": lang,
            "input": input,
            "user_email": user_email,
        }

        response = self._session.post(f"{self._url}/codes/", data=body)

        if response.status_code != HTTPStatus.CREATED:
            raise RuntimeError(runtime_error(response))

        data = response.json()

        return CodeFile.from_dict(dikt=data)

    def update_code(self, source: str, user_email: str, lang: str, input: str):
        body = {
            "source": source,
            "lang": lang,
            "input": input,
            "user_email": user_email,
        }

        # ? Patch or Put
        response = self._session.put(f"{self._url}/codes/", data=body)

        if response.status_code != HTTPStatus.CREATED:
            raise RuntimeError(runtime_error(response))

        data = response.json()

        return CodeFile.from_dict(dikt=data)


def get_idecore_exapi():
    return IdeCoreExApi(url=Config.IDE_CORE_URL)
