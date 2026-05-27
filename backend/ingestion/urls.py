from rest_framework.routers import DefaultRouter
from .views import RawUploadViewSet

router = DefaultRouter()
router.register("uploads", RawUploadViewSet, basename="upload")
urlpatterns = router.urls
