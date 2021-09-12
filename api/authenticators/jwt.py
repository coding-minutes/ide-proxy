from rest_framework import authentication
from exapi.olympus.models import Profile
from exapi.olympus.service import get_olympus_exapi


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        jwt = request.headers.get("Authorization")

        if jwt:
            _, jwt = jwt.split(" ")
            verified = get_olympus_exapi().verify_token(jwt=jwt)
            if verified:
                profile = Profile.from_jwt(jwt)
                return profile, jwt

        return None, None
