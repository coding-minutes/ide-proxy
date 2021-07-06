import requests
from http import HTTPStatus

from utils.requests import ExRequestSession
from exapi.ide_core.models import CodeFile
from utils.error import mk_runtime_error
from ide_proxy.config import Config


class IdeCoreExApi:
    def __init__(self, url: str):
        self._url = url
        self._session = ExRequestSession()

    def get_code(self, code_id: int):
        response = self._session.get(f"{self._url}/api/codes/{code_id}")

        if response.status_code != HTTPStatus.OK:
            raise RuntimeError(mk_runtime_error(response))

        res = response.json()
        data = res["data"]

        return CodeFile.from_dict(dikt=data)

    def save_code(self, source: str, user_email: str, lang: str, input: str):
        body = {
            "source": source,
            "lang": lang,
            "input": input,
            "user_email": user_email,
        }

        response = self._session.post(f"{self._url}/api/upsert/", json=body)

        if response.status_code != HTTPStatus.CREATED:
            raise RuntimeError(mk_runtime_error(response))

        parsed_response = response.json()
        x = parsed_response["data"]

        return CodeFile.from_dict(dikt=x)

    def update_code(self, source: str, lang: str, input: str, code_id: int):
        body = {"id": code_id}
        if source:
            body["source"] = source
        if lang:
            body["lang"] = lang
        if input:
            body["input"] = input

        response = self._session.post(f"{self._url}/api/upsert/", json=body)

        if response.status_code != HTTPStatus.OK:
            raise RuntimeError(mk_runtime_error(response))

        parsed_response = response.json()
        data = parsed_response["data"]

        return CodeFile.from_dict(dikt=data)


def get_idecore_exapi():
    return IdeCoreExApi(url=Config.IDE_CORE_URL)
