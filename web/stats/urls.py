from django.urls import path

from .views import StatView


app_name = "stats"

urlpatterns = [
    path("", StatView.as_view(), name="list"),
]
