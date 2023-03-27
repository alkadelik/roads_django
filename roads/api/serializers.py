from roads.models import Roads, Addresses
from rest_framework import serializers

class RoadsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roads
        # fields = ['route', 'segment', 'start_point', 'start_lat', 'start_lng', 'end_point', 'end_lat', 'end_lng', 'road_name', 'distance', 'travel_time', 'avg_speed', 'status']
        fields = '__all__'

class AddressesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addresses
        fields = '__all__'