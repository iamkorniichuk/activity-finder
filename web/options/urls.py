from rest_framework.routers import DefaultRouter

from .viewsets import OptionViewSet


app_name = "options"


router = DefaultRouter()
router.register("", OptionViewSet, "option")

urlpatterns = router.urls
