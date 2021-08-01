from django.urls import path
from utils.views import proxy
from ide_proxy.config import Config
from api.views.judge.views import RunView, SubmissionView


urlpatterns = [
    path("languages", proxy(url=f"{Config.JUDGE_PROXY_URL}/api/languages")),
    path("stubs", proxy(url=f"{Config.JUDGE_PROXY_URL}/api/stubs")),
    path("run", RunView.as_view()),
    path("submissions/<submission_id>", SubmissionView.as_view()),
]
