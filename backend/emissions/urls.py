from rest_framework.routers import DefaultRouter
from .views import EmissionRecordViewSet, NormalizationRuleViewSet

router = DefaultRouter()
router.register("records", EmissionRecordViewSet, basename="emission-record")
router.register("normalization-rules", NormalizationRuleViewSet, basename="normalization-rule")
urlpatterns = router.urls
