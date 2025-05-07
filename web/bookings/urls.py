from rest_framework.routers import DefaultRouter

from .viewsets import BookingViewSet


app_name = "bookings"


router = DefaultRouter()
router.register("", BookingViewSet, "booking")

urlpatterns = router.urls
