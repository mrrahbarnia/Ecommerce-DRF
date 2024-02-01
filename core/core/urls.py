from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import (
    path,
    include
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView
)

# Health Check for CICD automation
from rest_framework.views import APIView
from rest_framework.response import Response


class HealthCheck(APIView):

    def get(self, request, *args, **kwargs):
        return Response("CICD process works correctly.")


urlpatterns = [
    path('admin/', admin.site.urls),
    # ============ CICD Health Check ============ #
    path('health-check/', HealthCheck.as_view()),
    # ============ Accounts app ============ #
    path('api/v1/accounts/', include('accounts.api.v1.urls')),

    # ============ Product app ============ #
    path('api/v1/product/', include('product.api.v1.urls')),

    # ============ Django debug toolbar URL ============ #
    path("__debug__/", include("debug_toolbar.urls")),

    # ============ Swagger API documentation ============ #
    path('api/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/schema/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
