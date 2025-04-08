from rest_framework.routers import DefaultRouter

from .viewsets import ScheduleViewSet


app_name = "schedules"


router = DefaultRouter()
router.register("", ScheduleViewSet, "schedule")

urlpatterns = router.urls
