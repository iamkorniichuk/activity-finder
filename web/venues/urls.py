from rest_framework.routers import DefaultRouter

from .viewsets import VenueViewSet


app_name = "venues"


router = DefaultRouter()
router.register("", VenueViewSet, "venue")

urlpatterns = router.urls
