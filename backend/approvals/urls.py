from rest_framework.routers import DefaultRouter
from .views import ApprovalWorkflowViewSet

router = DefaultRouter()
router.register("", ApprovalWorkflowViewSet, basename="approval")
urlpatterns = router.urls
