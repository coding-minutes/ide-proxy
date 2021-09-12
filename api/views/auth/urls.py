from django.urls import path

from api.views.auth.views import LoginView, VerifyAuthenticationView


urlpatterns = [
    path("login", LoginView.as_view()),
    path("verify", VerifyAuthenticationView.as_view()),
]
