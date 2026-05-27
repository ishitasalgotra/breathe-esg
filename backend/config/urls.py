from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import TenantTokenObtainPairView, MeView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/login/", TenantTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/me/", MeView.as_view(), name="me"),
    path("api/tenants/", include("tenants.urls")),
    path("api/ingestion/", include("ingestion.urls")),
    path("api/emissions/", include("emissions.urls")),
    path("api/approvals/", include("approvals.urls")),
    path("api/audit/", include("audit.urls")),
]
