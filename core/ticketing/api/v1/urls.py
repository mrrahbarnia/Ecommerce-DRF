"""
URL's of the Ticketing app.
"""
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('ticketing', views.TicketApiViewSet, basename='ticketing')

urlpatterns = [
]
urlpatterns += router.urls