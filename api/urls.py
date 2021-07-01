from django.urls import path

from api.views import PingPongView, FetchCodeView, SaveCodeView, UpdateCodeView


urlpatterns = [
    path("ping/", PingPongView.as_view()),
    path('code/<int:pk>',FetchCodeView.as_view()),
    path('code/',SaveCodeView.as_view()),
    path('update/<int:pk>',UpdateCodeView.as_view()),
]
