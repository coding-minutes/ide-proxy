from dataclasses import dataclass
import jwt


@dataclass
class Profile:
    first_name: str
    last_name: str
    email: str
    photo: str
    id: str

    @classmethod
    def from_dict(cls, dikt):
        return cls(
            first_name=dikt.get("first_name"),
            last_name=dikt.get("last_name"),
            email=dikt.get("email"),
            photo=dikt.get("photo"),
            id=dikt.get("id"),
        )

    @classmethod
    def from_jwt(cls, token):
        decoded = jwt.decode(token, options={"verify_signature": False})
        return cls.from_dict(decoded)
