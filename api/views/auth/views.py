from rest_framework.views import APIView
from domain.services.authentication import get_google_authenticator
from utils.jwt import encode
from rest_framework.response import Response


class GoogleAuthenticateView(APIView):
    def post(self, request):
        token = request.data.get("token")
        user = get_google_authenticator().authenticate(google_jwt_token=token)
        encoded = encode(user.to_dict())
        return Response({"jwt": encoded}, status=200)
