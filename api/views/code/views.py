from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from domain.models import User
from api.mixins.permissions import IsAuthenticated
from exapi.ide_core.service import get_idecore_exapi


class CodeFileSerializer(serializers.Serializer):
    source = serializers.CharField()
    lang = serializers.CharField()
    input = serializers.CharField(default="")
    id = serializers.CharField(
        max_length=4, read_only=True, required=False, allow_null=True
    )
    title = serializers.CharField()


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

        user = request.user

        code = get_idecore_exapi().update_code(
            source=data.get("source"),
            lang=data.get("lang"),
            input=data.get("input"),
            code_id=code_id,
            user_email=user.email,
        )
        serializer = CodeFileSerializer(code)
        data = serializer.data

        return Response(data, status=200)


class SaveCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        user: User = request.user

        code = get_idecore_exapi().save_code(
            source=data["source"],
            user_email=user.email,
            lang=data["lang"],
            input=data["input"],
        )
        serializer = CodeFileSerializer(code)
        data = serializer.data

        return Response(data, status=201)


class SavedCodeListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        query = request.query_params.get("query", "")
        page = request.query_params.get("page", 1)

        res = get_idecore_exapi().get_saved_list(
            user_email=user.email, query=query, page=page
        )
        serializer = CodeFileSerializer(res["data"], many=True)
        res["data"] = serializer.data
        return Response(
            res,
            status=200,
        )
