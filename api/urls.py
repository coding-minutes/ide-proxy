from django.urls import path, include


urlpatterns = [
    path("code/", include("api.views.code.urls")),
]
