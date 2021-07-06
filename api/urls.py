from django.urls import path, include


urlpatterns = [
    path("code/", include("api.views.code.urls")),
    path("judge/", include("api.views.judge.urls")),
]
