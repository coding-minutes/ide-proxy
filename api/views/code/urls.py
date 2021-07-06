from django.urls import path

from api.views.code.views import FetchUpdateCodeView, SaveCodeView, PingPongView


urlpatterns = [
    path("ping", PingPongView.as_view()),
    path("<int:pk>", FetchUpdateCodeView.as_view()),
    path("", SaveCodeView.as_view()),
]
