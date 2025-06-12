from __future__ import annotations

from api.user.views import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AgencyViewSet, StopViewSet, RouteViewSet,
    ServiceViewSet, TripViewSet, StopTimeViewSet
)
from .views import gtfs_export_download
urlpatterns = [
    *router.urls,
]
urlpatterns = [
    path('api/', include(router.urls)),
]
urlpatterns += [
    path('api/gtfs/download/', gtfs_export_download, name='gtfs-export'),
]