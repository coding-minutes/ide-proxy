from rest_framework.views import APIView
from rest_framework.response import Response
from exapi.olympus.service import get_olympus_exapi


class LoginView(APIView):
    def post(self, request):
        data = request.data
        strategy = data.pop("strategy", "google")
        jwt = get_olympus_exapi().signin_with_token(data=data, strategy=strategy)
        return Response({"jwt": jwt}, status=200)


class VerifyAuthenticationView(APIView):
    def post(self, request):
        user = request.user
        if user:
            return Response(
                {
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "id": user.id,
                },
                status=200,
            )
        return Response({"message": "Invalid Token"}, status=401)
