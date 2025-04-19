from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path(
        "schema/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),
    path("activities/", include("activities.urls"), name="activities"),
    path("auth/", include("authentication.urls"), name="authentication"),
    path("schedules/", include("schedules.urls"), name="schedules"),
    path("territories/", include("territories.urls"), name="territories"),
    path("users/", include("users.urls"), name="users"),
    path("venues/", include("venues.urls"), name="venues"),
]
