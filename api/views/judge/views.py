from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from exapi.judge.service import get_judge_exapi
from api.serializers.base import BaseSerializer


class SubmissionSerializer(BaseSerializer):
    time = serializers.CharField()
    memory = serializers.IntegerField()
    stdout = serializers.CharField()
    stderr = serializers.CharField()
    compile_output = serializers.CharField()


class SubmissionDeserializer(serializers.Serializer):
    source_code = serializers.CharField()
    language_id = serializers.IntegerField()
    stdin = serializers.CharField(allow_blank=True, required=False)


class RunView(APIView):
    def post(self, request):
        submission = SubmissionDeserializer(data=request.data)
        submission.is_valid(raise_exception=True)
        submission = submission.validated_data

        submission_id = get_judge_exapi().run_code(
            source_code=submission.get("source_code"),
            language_id=submission.get("language_id"),
            stdin=submission.get("stdin"),
        )

        return Response({"submission_id": submission_id})


class SubmissionView(APIView):
    def get(self, request, submission_id):
        submission = get_judge_exapi().get_submission(submission_id=submission_id)

        serializer = SubmissionSerializer(submission)

        return Response(serializer.data)
