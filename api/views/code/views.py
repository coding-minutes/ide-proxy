from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from api.mixins.permissions import IsAuthenticated
from exapi.ide_core.service import get_idecore_exapi

from utils.validator import body_validator


class CodeFileSerializer(serializers.Serializer):
    source = serializers.CharField()
    lang = serializers.CharField()
    input = serializers.CharField(default="", allow_blank=True)
    id = serializers.CharField(
        max_length=4, read_only=True, required=False, allow_null=True
    )
    title = serializers.CharField()
    created_at = serializers.DateField(read_only=True)
    updated_at = serializers.DateField(read_only=True)


class FetchUpdateCodeView(APIView):
    def get(self, request, **kwargs):
        code_id = self.kwargs["pk"]

        code = get_idecore_exapi().get_code(code_id=code_id)
        serializer = CodeFileSerializer(code)
        data = serializer.data

        return Response(data, status=200)

    @body_validator(serializer_class=CodeFileSerializer)
    def patch(self, request, validated_data, **kwargs):
        data = validated_data
        code_id = self.kwargs["pk"]

        user = request.user

        code = get_idecore_exapi().update_code(
            source=data.get("source"),
            lang=data.get("lang"),
            input=data.get("input"),
            code_id=code_id,
            user_email=user.email,
            title=data.get("title"),
        )
        serializer = CodeFileSerializer(code)
        data = serializer.data

        return Response(data, status=200)


class SaveCodeView(APIView):
    permission_classes = [IsAuthenticated]

    @body_validator(serializer_class=CodeFileSerializer)
    def post(self, request, validated_data):
        data = validated_data
        user = request.user

        code = get_idecore_exapi().save_code(
            source=data["source"],
            user_email=user.email,
            lang=data["lang"],
            input=data["input"],
            title=data["title"],
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
