from rest_framework.routers import DefaultRouter

from .viewsets import LayoutViewSet


app_name = "layouts"


router = DefaultRouter()
router.register("", LayoutViewSet, "layout")

urlpatterns = router.urls
