from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response


class PingPongView(APIView):
    def get(self, request):
        return Response({"message": "pong"})