from rest_framework.routers import DefaultRouter

from .viewsets import UserViewSet


app_name = "users"


router = DefaultRouter()
router.register("", UserViewSet, "user")

urlpatterns = router.urls
