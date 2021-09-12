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

    def get_code(self, code_id: str):
        response = self._session.get(f"{self._url}/api/codes/{code_id}")

        if response.status_code != HTTPStatus.OK:
            raise RuntimeError(mk_runtime_error(response))

        res = response.json()
        data = res["data"]

        return CodeFile.from_dict(dikt=data)

    def save_code(self, source: str, user_email: str, lang: str, input: str, title: str):
        body = {
            "source": source,
            "lang": lang,
            "input": input,
            "user_email": user_email,
            "title": title
        }

        response = self._session.post(f"{self._url}/api/upsert/", json=body)

        if response.status_code != HTTPStatus.CREATED:
            raise RuntimeError(mk_runtime_error(response))

        parsed_response = response.json()
        data = parsed_response["data"]

        return CodeFile.from_dict(dikt=data)

    def update_code(
        self, source: str, lang: str, input: str, code_id: str, user_email: str, title: str
    ):
        body = {"id": code_id}
        if source:
            body["source"] = source
        if lang:
            body["lang"] = lang
        if input:
            body["input"] = input
        if title:
            body["title"] = title

        # Verify whether current user owns the saved code.
        response = self._session.get(f"{self._url}/api/codes/{code_id}")
        res = response.json()
        data = res["data"]

        # If the current user is now the owner of the saved code, then save and return new code for current user.
        if data["user_email"] != user_email:
            return self.save_code(
                source=body.get("source", data["source"]),
                user_email=user_email,
                lang=body.get("lang", data["lang"]),
                input=body.get("input", data["input"]),
            )

        # Otherwise proceed with the patch update.

        response = self._session.post(f"{self._url}/api/upsert/", json=body)

        if response.status_code != HTTPStatus.OK:
            raise RuntimeError(mk_runtime_error(response))

        parsed_response = response.json()
        data = parsed_response["data"]

        return CodeFile.from_dict(dikt=data)

    def get_saved_list(self, user_email, query="", page=1):
        params = {"user_email": user_email, "query": query, "page": page}
        response = self._session.get(url=f"{self._url}/api/saved/", params=params)

        if response.status_code != HTTPStatus.OK:
            raise RuntimeError(mk_runtime_error(response))

        res = response.json()
        data = res["data"]

        res["data"] = [CodeFile.from_dict(dikt=code) for code in data]
        return res


def get_idecore_exapi():
    return IdeCoreExApi(url=Config.IDE_CORE_URL)
