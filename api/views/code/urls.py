from django.urls import path

from api.views.code.views import FetchUpdateCodeView, SaveCodeView, SavedCodeListView


urlpatterns = [
    path("saved", SavedCodeListView.as_view()),
    path("<pk>", FetchUpdateCodeView.as_view()),
    path("", SaveCodeView.as_view()),
]
