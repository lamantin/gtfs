from __future__ import annotations

from django.contrib.auth.models import AbstractUser

from django.db import models

# 1. Szolgáltató (Agency)
class Agency(models.Model):
    agency_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    url = models.URLField()
    timezone = models.CharField(max_length=50)
    lang = models.CharField(max_length=2, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


# 2. Megálló (Stop)
class Stop(models.Model):
    stop_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    lat = models.FloatField()
    lon = models.FloatField()
    location_type = models.SmallIntegerField(default=0)  # 0: stop, 1: station
    parent_station = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


# 3. Útvonal (Route)
class Route(models.Model):
    route_id = models.CharField(max_length=50, unique=True)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    short_name = models.CharField(max_length=50, blank=True, null=True)
    long_name = models.CharField(max_length=255, blank=True, null=True)
    route_type = models.SmallIntegerField(default=3)  # 3: busz
    color = models.CharField(max_length=6, blank=True, null=True)
    text_color = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return self.short_name or self.long_name or self.route_id


# 4. Naptár (Service/Calendar)
class Service(models.Model):
    service_id = models.CharField(max_length=50, unique=True)
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.service_id


# 5. Járat (Trip)
class Trip(models.Model):
    trip_id = models.CharField(max_length=50, unique=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    headsign = models.CharField(max_length=255, blank=True, null=True)
    direction_id = models.SmallIntegerField(blank=True, null=True)
    shape_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.trip_id


# 6. Megállók sorrendje és időzítése (StopTime)
class StopTime(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    stop_sequence = models.IntegerField()
    arrival_time = models.TimeField()
    departure_time = models.TimeField()
    pickup_type = models.SmallIntegerField(default=0)
    drop_off_type = models.SmallIntegerField(default=0)

    class Meta:
        unique_together = ('trip', 'stop_sequence')
        ordering = ['trip', 'stop_sequence']


# 7. Útvonal forma (Shape) – opcionális, térképes megjelenítéshez
class Shape(models.Model):
    shape_id = models.CharField(max_length=50)
    lat = models.FloatField()
    lon = models.FloatField()
    sequence = models.IntegerField()

    class Meta:
        ordering = ['shape_id', 'sequence']

class User(AbstractUser):
    pass
