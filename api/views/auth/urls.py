from django.urls import path

from api.views.auth.views import GoogleAuthenticateView


urlpatterns = [path("login", GoogleAuthenticateView.as_view())]
