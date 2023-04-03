# DRF imports
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

# python imports
import json
from urllib.parse import urlencode

# other imports
import requests # requests installed by pip
from decouple import config

# app imports
from roads.models import Segment, Addresses, Route
from roads.api.serializers import SegmentSerializer, AddressesSerializer, RouteSerializer

@api_view(['GET', 'POST'])
def roads_list(request):
    if request.method == 'GET':
        roads = Segment.objects.all().order_by('route')
        serializer = SegmentSerializer(roads, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SegmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def roads_detail(request, pk):
    try:
        road = Segment.objects.get(pk=pk)
    except Segment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SegmentSerializer(roads)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SegmentSerializer(roads, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errrors, status=status.HTTP_404_BAD_REQUEST)

    elif request.method == 'DELETE':
        road.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def road_status(request):
    if request.method == 'POST':
        try:
            start_lat = request.data.get("start_lat")
            start_lng = request.data.get("start_lng")
            end_lat = request.data.get("end_lat")
            end_lng = request.data.get("end_lng")
        except:
            return Response({'error': 'Please provide an origin and a destination'},
                        status=HTTP_400_BAD_REQUEST)

    # for each segment
        # extract the pairs of longitudes and latitudes
        # call google
    key = config('GOOGLE_ROUTES_API_KEY')
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=' + start_lat + '%2C' + start_lng + '&destinations=' + end_lat + '%2C' + end_lng + '&key=' + key
    # url should have options and should be computed better
    
    payload={}
    header = {}  

    response = requests.get(url, data=payload, headers=header).json()

    origin_address = response['origin_addresses'][0]
    destination_address = response['destination_addresses'][0]
    distance = response['rows'][0]['elements'][0]['distance']['text'][:-2]
    duration = response['rows'][0]['elements'][0]['duration']['text'][:-4]
    duration2 = round((float(duration) / 60), 2) # converted from mins to hrs - used for calculating speed
    speed = round((float(distance) / duration2), 0)

    # I tried to use get_or_create for this but running into unique constraint errors
    try:
        start_point = Addresses.objects.get(address = origin_address)
    except:
        start_point = Addresses.objects.create(
            address = origin_address,
            lat = start_lat,
            lng = start_lng
        )

    try:
        end_point = Addresses.objects.get(address = destination_address)
    except:
        end_point = Addresses.objects.create(
            address = destination_address,
            lat = start_lat,
            lng = start_lng
        )

    if speed < 50: # ~30mph
        status = 1 #'bad' 
    elif speed < 65: # ~40mph
        status = 2 #'poor'
    elif speed < 80: # ~50mph
        status = 3 #'ok'
    elif speed < 95: # ~60mph
        status = 4 #'good'
    elif speed < 110: # ~70mph
        status = 5 #'very good'
    elif speed < 125: # ~80mph
        status = 5 #'Excellent'
  
    # - if not in db, add to db
    road, created = Segment.objects.get_or_create(
        # route = 
        # segment = 
        start_point = start_point,
        end_point = end_point,
        road_name = '',
        distance = distance,
        travel_time = duration,
        avg_speed = speed,
        # direction
        status = status
    )

    # route = models.CharField(max_length=10, default='A00')

    # - automate when the roads should automatically be updated 

    # if (
    #     response.status_code != 204 and
    #     response.headers["content-type"].strip().startswith("application/json")
    # ):
    #     try:
    #         return response.json()
    #     except ValueError:
    #         # decide how to handle a server that's misbehaving to this extent
    not_created = {
        'message': "This road already exists",
        'road': road
    }

    # if not created:
    #     return Response({'data': not_created}, status=HTTP_200_OK)
    # else:
    #     return Response({'data': response}, status=HTTP_200_OK)
    return Response({'data': response}, status=HTTP_200_OK)

@api_view(['GET', 'POST'])
def bulk_segments_upload(request):
    if request.method == 'POST':
        # try:
        #     for obj in request.data: # figure how to bulk_create() this
        #         Route.objects.get_or_create(
        #             segment=obj.get("ROUTE"),
        #         )
        # except:
        #     return Response({'error': 'Could not create routes'}, status=HTTP_200_OK)

        try:
            # 1. Save segments
            # default_address = Addresses.objects.get(pk=14)
            addresses = []
            for obj in request.data: # figure how to bulk_create() this
                batch = {
                    'segment': obj.get("SEGMENT_CO"),
                    'start_lat': json.dumps(obj.get("NORTHINGS")),
                    'start_lng': json.dumps(obj.get("EASTINGS")),
                    'end_lat': json.dumps(obj.get("NORTHINGS2")),
                    'end_lng': json.dumps(obj.get("EASTINGS2"))
                }
                addresses.append(batch)

        except:
            print("excepting")
            return Response({'error': 'Could not create addresses'}, status=HTTP_200_OK)


    google_addresses = []
    segments = []
    for point in addresses:
        try:
            # 2. Fetch segment parameters from Google
            key = config('GOOGLE_ROUTES_API_KEY')
            url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=' + point['start_lat'] + '%2C' + point['start_lng'] + '&destinations=' + point['end_lat'] + '%2C' + point['end_lng'] + '&key=' + key

            payload={}
            header = {}  

            response = requests.get(url, data=payload, headers=header).json()

            # 3. Save addresses2
            start_point = Addresses(
                address = response['origin_addresses'][0],
                lat = point['start_lat'],
                lng = point['start_lng']
            )
            google_addresses.append(start_point)

            end_point = Addresses( # might not need to add this since the end point of one, is the starting point of another
                address = response['destination_addresses'][0],
                lat = point['end_lat'],
                lng = point['end_lng']
            )
            google_addresses.append(end_point)

            # 4. Create segments with distance, speed, and time of travel
            distance = response['rows'][0]['elements'][0]['distance']['text'][:-2]
            duration = response['rows'][0]['elements'][0]['duration']['text'][:-4]
            duration2 = round((float(duration) / 60), 2) # converted from mins to hrs - used for calculating speed
            speed = round((float(distance) / duration2), 0)

            if speed < 50: # ~30mph
                status = 1 #'bad' 
            elif speed < 65: # ~40mph
                status = 2 #'poor'
            elif speed < 80: # ~50mph
                status = 3 #'ok'
            elif speed < 95: # ~60mph
                status = 4 #'good'
            elif speed < 110: # ~70mph
                status = 5 #'very good'
            elif speed < 125: # ~80mph
                status = 5 #'Excellent'

            segments.append(Segment(
                segment = point['segment'],
                road_name = '',
                start_point = Addresses.objects.filter(lat=point['start_lat'], lng=point['start_lng'])[:1].get(),
                end_point = Addresses.objects.filter(lat=point['end_lat'], lng=point['end_lng']).first(),
                distance = distance,
                travel_time = duration,
                avg_speed = speed,
                status = status
            ))

        except:
            print("excepting 2")
            return Response({'error': 'Could not fetch details from google'}, status=HTTP_200_OK)

    Addresses.objects.bulk_create(google_addresses, ignore_conflicts=True)
    Segment.objects.bulk_create(segments, ignore_conflicts=True)

    # return Response({'data': response}, status=HTTP_200_OK)
    return Response({'response': batch}, status=HTTP_200_OK)