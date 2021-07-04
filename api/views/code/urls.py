from django.urls import path

from api.views.code.views import FetchUpdateCodeView, SaveCodeView


urlpatterns = [
    path("<int:pk>", FetchUpdateCodeView.as_view()),
    path("", SaveCodeView.as_view()),
]
