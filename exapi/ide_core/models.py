from typing import Dict, Optional, Union
from dataclasses import dataclass


@dataclass
class CodeFile:
    source: str
    user_email: str
    lang: str
    input: str
    id: str
    title: str

    @classmethod
    def from_dict(cls, dikt: Dict) -> "CodeFile":
        return cls(
            source=dikt["source"],
            user_email=dikt["user_email"],
            lang=dikt["lang"],
            input=dikt["input"],
            id=dikt.get("id", None),
            title=dikt["title"],
        )
