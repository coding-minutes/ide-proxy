from django.urls import path, include


urlpatterns = [
    path("code/", include("api.views.code.urls")),
    path("judge/", include("api.views.judge.urls")),
    path("auth/", include("api.views.auth.urls")),
]
