from typing import Dict, Optional
from requests import Request, Session


class ExRequestSession(Session):
    _headers: Dict
    _timeout: int

    def __init__(self, headers: Dict = {}, timeout: Optional[int] = None):
        super().__init__()
        self._headers = headers
        self._timeout = timeout

    def request(self, *args, **kwargs) -> Request:
        current_headers = kwargs.pop("headers", {})
        headers = {**self._headers, **current_headers}

        timeout = kwargs.pop("timeout", self._timeout)

        return super().request(*args, **kwargs, headers=headers, timeout=timeout)
