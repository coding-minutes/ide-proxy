import requests
from http import HTTPStatus
from typing import List
from utils.error import mk_runtime_error
from exapi.judge.models import Submission
from ide_proxy.config import Config


class JudgeExapi:
    def __init__(self, url: str):
        self._url = url

    def run_code(self, source_code, language_id, stdin) -> str:
        payload = {
            "source_code": source_code,
            "language_id": language_id,
            "stdin": stdin,
        }
        response = requests.post(f"{self._url}/api/run", json=payload)

        if response.status_code != HTTPStatus.OK:
            raise RuntimeError(mk_runtime_error(response))

        return response.json()["submission_id"]

    def get_submission(self, submission_id) -> Submission:
        response = requests.get(f"{self._url}/api/submissions/{submission_id}")

        if response.status_code == HTTPStatus.NOT_FOUND:
            return None

        if response.status_code != HTTPStatus.OK:
            raise RuntimeError(mk_runtime_error(response))

        data = response.json()["data"]

        return Submission.from_dict(data)


def get_judge_exapi():
    return JudgeExapi(url=Config.JUDGE_PROXY_URL)
