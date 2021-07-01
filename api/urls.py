from django.urls import path

from api.views import PingPongView


urlpatterns = [path("ping/", PingPongView.as_view())]