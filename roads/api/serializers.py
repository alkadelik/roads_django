from roads.models import Segment, Addresses, Route
from rest_framework import serializers

class SegmentSerializer(serializers.ModelSerializer):
    # map = serializers.ImageField(max_length=None, allow_empty_file=False, allow_null=True, required=False, use_url=True )
    map = serializers.ImageField(max_length=None, allow_empty_file=False)

    class Meta:
        model = Segment
        fields = '__all__'

class AddressesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addresses
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        # fields = ['route',]
        fields = '__all__'