import requests
from http import HTTPStatus

from utils.requests import ExRequestSession
from api.exapi.judge0.models import Submission
from judge_proxy.config import Config


class Judge0ExApi:
    def __init__(self, url: str):
        headers = {"X-Auth-Token": "something"}

        self._url = url
        self._session = ExRequestSession(headers=headers)

    def create_submission(self, source_code: str, language_id: int, stdin: str) -> str:
        params = {"base64_encoded": "true"}
        body = {"source_code": source_code, "language_id": language_id, "stdin": stdin}
        response = self._session.post(
            f"{self._url}/submissions", params=params, json=body
        )

        if response.status_code != HTTPStatus.CREATED:
            raise RuntimeError(
                f"""
                Runtime Error
                Message: {response.content.decode("utf-8")}
                Status Code: {response.status_code}
            """
            )

        data = response.json()

        return data["token"]

    def get_submission(self, submission_token: str) -> Submission:
        params = {"base64_encoded": "true"}
        response = self._session.get(
            f"{self._url}/submissions/{submission_token}", params=params
        )

        if response.status_code != HTTPStatus.OK:
            raise RuntimeError(
                f"""
                Runtime Error
                Message: {response.content.decode("utf-8")}
                Status Code: {response.status_code}
            """
            )

        data = response.json()

        return Submission.from_dict(dikt=data)


def get_judge0_exapi():
    return Judge0ExApi(url=Config.JUDGE0_URL)