import jwt
from typing import Dict, Any


def encode(data: Dict[str, Any]):
    encoded = jwt.encode(data, "abc")
    return encoded


def decode(token: str):
    decoded = jwt.decode(token, "abc", algorithms=["HS256"])
    return decoded
