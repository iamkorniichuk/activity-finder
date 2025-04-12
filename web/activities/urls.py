from rest_framework.routers import DefaultRouter

from .viewsets import ActivityViewSet


app_name = "activities"


router = DefaultRouter()
router.register("", ActivityViewSet, "activity")

urlpatterns = router.urls
