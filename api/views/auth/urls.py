from django.urls import path

from api.views.auth.views import GoogleAuthenticateView, VerifyAuthenticationView


urlpatterns = [
    path("login", GoogleAuthenticateView.as_view()),
    path("verify", VerifyAuthenticationView.as_view()),
]
