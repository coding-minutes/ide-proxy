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


class VerifyAuthenticationView(APIView):
    def post(self, request):
        user = request.user
        if user:
            return Response(
                {
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
                status=200,
            )
        return Response({"message": "Invalid Token"}, status=401)
