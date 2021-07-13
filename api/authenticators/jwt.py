from rest_framework import authentication
from domain.models import User
from utils.jwt import decode


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        jwt = request.headers.get("Authorization")

        if jwt:
            _, jwt = jwt.split(" ")
            decoded = decode(jwt)
            user = User.from_dict(decoded)
            return user, jwt

        return None, None
