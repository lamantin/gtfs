from __future__ import annotations

from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db import models


class Agency(models.Model):
    agency_id: str = models.CharField(max_length=50, unique=True)
    name: str = models.CharField(max_length=255)
    url: str = models.URLField()
    timezone: str = models.CharField(max_length=50)
    lang: str = models.CharField(max_length=2, blank=True)
    phone: str = models.CharField(max_length=50, blank=True)

    def __str__(self) -> str:
        return self.name


class Stop(models.Model):
    stop_id: str = models.CharField(max_length=50, unique=True)
    name: str = models.CharField(max_length=255)
    lat: float = models.FloatField()
    lon: float = models.FloatField()
    location_type: int = models.SmallIntegerField(default=0)  # 0: stop, 1: station
    parent_station: str = models.CharField(max_length=50, blank=True)

    def __str__(self) -> str:
        return self.name


class Route(models.Model):
    route_id: str = models.CharField(max_length=50, unique=True)
    agency: Agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    short_name: str = models.CharField(max_length=50, blank=True)
    long_name: str = models.CharField(max_length=255, blank=True)
    route_type: int = models.SmallIntegerField(default=3)  # 3: bus
    color: str = models.CharField(max_length=6, blank=True)
    text_color: str = models.CharField(max_length=6, blank=True)

    def __str__(self) -> str:
        return self.short_name or self.long_name or self.route_id


class Service(models.Model):
    service_id: str = models.CharField(max_length=50, unique=True)
    monday: bool = models.BooleanField(default=False)
    tuesday: bool = models.BooleanField(default=False)
    wednesday: bool = models.BooleanField(default=False)
    thursday: bool = models.BooleanField(default=False)
    friday: bool = models.BooleanField(default=False)
    saturday: bool = models.BooleanField(default=False)
    sunday: bool = models.BooleanField(default=False)
    start_date: models.DateField = models.DateField()
    end_date: models.DateField = models.DateField()

    def __str__(self) -> str:
        return self.service_id


class Trip(models.Model):
    trip_id: str = models.CharField(max_length=50, unique=True)
    route: Route = models.ForeignKey(Route, on_delete=models.CASCADE)
    service: Service = models.ForeignKey(Service, on_delete=models.CASCADE)
    headsign: str = models.CharField(max_length=255, blank=True)
    direction_id: int = models.SmallIntegerField(blank=True)
    shape_id: str = models.CharField(max_length=50, blank=True)

    def __str__(self) -> str:
        return self.trip_id


class StopTime(models.Model):
    trip: Trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    stop: Stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    stop_sequence: int = models.IntegerField()
    arrival_time: models.TimeField = models.TimeField()
    departure_time: models.TimeField = models.TimeField()
    pickup_type: int = models.SmallIntegerField(default=0)
    drop_off_type: int = models.SmallIntegerField(default=0)

    class Meta:
        unique_together: ClassVar[tuple[str, ...]] = ("trip", "stop_sequence")
        ordering: ClassVar[list[str]] = ["trip", "stop_sequence"]

    def __str__(self) -> str:
        return f"{self.trip.trip_id} - {self.stop.name} ({self.stop_sequence})"


class Shape(models.Model):
    shape_id: str = models.CharField(max_length=50)
    lat: float = models.FloatField()
    lon: float = models.FloatField()
    sequence: int = models.IntegerField()

    class Meta:
        ordering: ClassVar[list[str]] = ["shape_id", "sequence"]

    def __str__(self) -> str:
        return f"{self.shape_id} - {self.sequence}"


class User(AbstractUser):
    ...
