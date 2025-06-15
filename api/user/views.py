from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

from django.http import FileResponse
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.common.routers import CustomViewRouter
from api.user import serializers
from api.user.models import User
from api.user.permissions import IsStaffPermission

from .models import Agency, Route, Service, Stop, StopTime, Trip
from .serializers import (
    AgencySerializer,
    RouteSerializer,
    ServiceSerializer,
    StopSerializer,
    StopTimeSerializer,
    TripSerializer,
)

if TYPE_CHECKING:
    from rest_framework.request import Request

router = CustomViewRouter()

logger = logging.getLogger(__name__)


class AgencyViewSet(viewsets.ModelViewSet):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer


class StopViewSet(viewsets.ModelViewSet):
    queryset = Stop.objects.all()
    serializer_class = StopSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer


class StopTimeViewSet(viewsets.ModelViewSet):
    queryset = StopTime.objects.all()
    serializer_class = StopTimeSerializer


@router.register(r"users/me/", name="users")
class MyUserView(GenericAPIView):
    serializer_class = serializers.UserSerializer

    def get(self, request: Request) -> Response:
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


@router.register(r"users", name="users")
class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsStaffPermission,)


@api_view(["GET"])
def gtfs_export_download() -> FileResponse | Response:
    zip_path = Path("static/gtfs_feed.zip")
    if zip_path.exists():
        return FileResponse(zip_path.open("rb"), content_type="application/zip")
    return Response({"detail": "GTFS feed not found."}, status=status.HTTP_404_NOT_FOUND)
