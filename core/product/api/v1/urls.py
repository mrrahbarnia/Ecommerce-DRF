"""
URL's for Accounts API's.
"""
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('product', views.ProductApiViewSet, basename='product')
router.register('brand', views.BrandApiViewSet, basename='brand')
router.register('type', views.ProductTypeApiViewSet, basename='product-type')

urlpatterns = [
]
urlpatterns += router.urls
