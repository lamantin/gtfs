from __future__ import annotations

from django.urls import include, path

from api.user.views import router

from .views import (
    gtfs_export_download,
)

urlpatterns = [
    *router.urls,
]
urlpatterns = [
    path("api/", include(router.urls)),
]
urlpatterns += [
    path("api/gtfs/download/", gtfs_export_download, name="gtfs-export"),
]
