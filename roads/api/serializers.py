from roads.models import Segment, Addresses, Route
from rest_framework import serializers

class SegmentSerializer(serializers.ModelSerializer):
    map = serializers.ImageField(max_length=None, allow_empty_file=True, allow_null=True, required=False, use_url=True )

    class Meta:
        model = Segment
        # fields = ['route', 'segment', 'start_point', 'start_lat', 'start_lng', 'end_point', 'end_lat', 'end_lng', 'road_name', 'distance', 'travel_time', 'avg_speed', 'status', 'map']
        fields = '__all__'

class AddressesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addresses
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = 'route'