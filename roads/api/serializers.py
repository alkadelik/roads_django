from roads.models import Segment, Addresses, Route
from rest_framework import serializers

class SegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Segment
        # fields = ['route', 'segment', 'start_point', 'start_lat', 'start_lng', 'end_point', 'end_lat', 'end_lng', 'road_name', 'distance', 'travel_time', 'avg_speed', 'status']
        fields = '__all__'

class AddressesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addresses
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = 'route'