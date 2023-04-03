from django.db import models

class Route(models.Model):
    route = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.route

class Addresses(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=128, unique=True)
    lat = models.DecimalField(max_digits=30, decimal_places=15, default=0.0)
    lng = models.DecimalField(max_digits=30, decimal_places=15, default=0.0)

    def __str__(self):
        return self.address

class Segment(models.Model):
    route = models.ManyToManyField(Route, blank=True)
    road_name = models.CharField(max_length=30, blank=True)
    segment = models.CharField(max_length=10, unique=True)
    start_point = models.ForeignKey(Addresses, to_field='address', related_name='start_point', on_delete=models.SET_DEFAULT, default=14) # default=14 is a "None" address with 0.0 lat/lng
    end_point = models.ForeignKey(Addresses, to_field='address', related_name='end_point', on_delete=models.SET_DEFAULT, default=14)
    distance = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    travel_time = models.IntegerField(default=0)
    avg_speed = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)
    # direction
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.segment

