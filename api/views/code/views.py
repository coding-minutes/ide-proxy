from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from exapi.ide_core.service import get_idecore_exapi


class PingPongView(APIView):
    def get(self, request):
        print(request.user)
        return Response({"message": "pong"})


class CodeFileSerializer(serializers.Serializer):
    source = serializers.CharField()
    lang = serializers.CharField()
    input = serializers.CharField(default="")
    user_email = serializers.EmailField()
    id = serializers.IntegerField(read_only=True, required=False, allow_null=True)


class FetchUpdateCodeView(APIView):
    def get(self, request, *args, **kwargs):
        code_id = self.kwargs["pk"]

        code = get_idecore_exapi().get_code(code_id=code_id)
        serializer = CodeFileSerializer(code)
        data = serializer.data

        return Response(data, status=200)

    def patch(self, request, *args, **kwargs):
        data = request.data
        code_id = self.kwargs["pk"]

        # * : user_email cannot be updated
        code = get_idecore_exapi().update_code(
            source=data.get("source"),
            lang=data.get("lang"),
            input=data.get("input"),
            code_id=code_id,
        )
        serializer = CodeFileSerializer(code)
        data = serializer.data

        return Response(data, status=200)


class SaveCodeView(APIView):
    # permission_classes = (IsAuthenticated,)
    def post(self, request):
        data = request.data

        # TODO: user_email must be fetched from request.user
        # TODO: but use this until authentication is set up
        code = get_idecore_exapi().save_code(
            source=data["source"],
            user_email=data["user_email"],
            lang=data["lang"],
            input=data["input"],
        )
        serializer = CodeFileSerializer(code)
        data = serializer.data

        return Response(data, status=201)
