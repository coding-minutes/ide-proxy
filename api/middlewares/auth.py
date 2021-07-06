from utils.jwt import decode
from domain.models import User

from django.utils.functional import SimpleLazyObject
from django.utils.deprecation import MiddlewareMixin

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        jwt = request.headers.get('Authorization')
        if jwt:
            _, jwt = jwt.split(' ')
            decoded = decode(jwt)
            request.user = SimpleLazyObject(lambda: User.from_dict(decoded))
            print(request)