from rest_framework.routers import DefaultRouter

from .viewsets import ReactionViewSet


app_name = "reactions"


router = DefaultRouter()
router.register("", ReactionViewSet, "reaction")

urlpatterns = router.urls
