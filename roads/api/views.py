# django imports
from django.db import IntegrityError

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
from roads.models import Segment, Address, Route
from roads.api.serializers import SegmentSerializer, AddressSerializer, RouteSerializer

@api_view(['GET', 'POST'])
def load_segments(request):
    if request.method == 'GET':
        segments = Segment.objects.all().order_by('state')
        segments_serializer = SegmentSerializer(segments, many=True)

        addresses = Address.objects.all()
        addresses_serializer = AddressSerializer(addresses, many=True)
        
        routes = Route.objects.all()
        routes_serializer = RouteSerializer(routes, many=True)

        try:
            for segment in segments_serializer.data:
                # it is important that the northings and eastings group is done first. After that,
                # the definition of segment['start_point'] changes and affects the code 
                segment['northings'] = addresses.filter(pk=segment['start_point']).values()[0]['lng']
                segment['eastings'] = addresses.filter(pk=segment['start_point']).values()[0]['lat']
                segment['northings2'] = addresses.filter(pk=segment['end_point']).values()[0]['lng']
                segment['eastings2'] = addresses.filter(pk=segment['end_point']).values()[0]['lat']

                segment['start_point'] = addresses.filter(pk=segment['start_point']).values()[0]['name']
                segment['end_point'] = addresses.filter(pk=segment['end_point']).values()[0]['name']
                segment['route'] = Route.objects.filter(pk=segment['route']).values()[0]['route']
            
        except:
            print('error occurreds getting route or start_point')
            pass

        context = {
            'segments': segments_serializer.data,
            'addresses': addresses_serializer.data,
            'routes': routes_serializer.data
        }
        return Response(context)

    elif request.method == 'POST':
        serializer = SegmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def routes_list_mod(request):
    if request.method == 'GET':
        routes = Route.objects.all().order_by('pk')
        serializer = RouteSerializer(routes, many=True)
        return Response(serializer.data)

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
        Route.objects.get_or_create(route=request.obj.get("ROUTE"))

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
    start_point = Address.objects.get_or_create(
        address = response['origin_addresses'][0],
        lat = start_lat,
        lng = start_lng,
        name = request.data.get('start_name')
    )


    end_point = Address.objects.get_or_create(
        address = response['destination_addresses'][0],
        lat = end_lat,
        lng = end_lng,
        name = request.data.get('end_name')
    )
    # try:
    #     start_point = Address.objects.get(address = origin_address)
    # except:
    #     start_point = Addresses.objects.create(
    #         address = origin_address,
    #         lat = start_lat,
    #         lng = start_lng
    #     )

    # try:
    #     end_point = Address.objects.get(address = destination_address)
    # except:
    #     end_point = Address.objects.create(
    #         address = destination_address,
    #         lat = start_lat,
    #         lng = start_lng
    #     )

    distance = response['rows'][0]['elements'][0]['distance']['text'][:-2]
    try:
        duration = response['rows'][0]['elements'][0]['duration']['text'][:-4]
        duration2 = round((float(duration) / 60), 2) # converted from mins to hrs - used for calculating speed
    except Exception as e: # ValueError: could not convert string to float:
        duration = response['rows'][0]['elements'][0]['duration']['text']
        split = duration.split()
        
        if len(split) < 3: # exactly single digit hour with no minutes e.g. 2 hours
            duration = int(split[0]) * 60
        else: # hour and minutes e.g. 2 hours 5 mins
            duration = (int(split[0]) * 60) + int(split[2])
    
    duration2 = round((float(duration) / 60), 2)
    speed = round((float(distance) / duration2), 0)

    if speed < 50: # ~40mph
        status = 'FF0000' # bad
    elif speed < 65: # ~40mph
        status = 'FF4081' # bad
    elif speed < 80: # ~50mph
        status = 'FF8000' #'poor'
    elif speed < 95: # ~60mph
        status = 'FFFF00' #'ok'
    elif speed < 110: # ~70mph
        status = '80FF00' #'good'
    else: # ~80mph
        status = '0A5D00' #'Excellent'
  
    # - if not in db, add to db
    road, created = Segment.objects.get_or_create(
        code = request.data.get("SEGMENT_CODE"),
        name = request.data.get("SEGMENT_NAME"),
        state = request.data.get("STATE"),
        distance = segment['distance'],
        travel_time = segment['travel_time'],
        avg_speed = segment['avg_speed'],
        status = segment['status'],
        start_point = Address.objects.filter(lat=addresses[i]['start_lat'], lng=addresses[i]['start_lng'])[:1].get(), # what is this .get() at the end?
        end_point = Address.objects.filter(lat=addresses[i]['end_lat'], lng=addresses[i]['end_lng']).first(),
        route = Route.objects.get(route=addresses[i]['route'])
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


    if request.method == 'POST':
        

        # 1. Save segments
        addresses = []
        for obj in request.data:
            batch = {
                'route': obj.get("ROUTE"),
                'code': obj.get("SEGMENT_CODE"),
                'start_lat': json.dumps(obj.get("NORTHINGS")),
                'start_lng': json.dumps(obj.get("EASTINGS")),
                'end_lat': json.dumps(obj.get("NORTHINGS2")),
                'end_lng': json.dumps(obj.get("EASTINGS2")),
                'start_name': obj.get("START_NAME"),
                'end_name': obj.get("END_NAME"),
                'name': obj.get("SEGMENT_NAME"),
                'state': obj.get("STATE"),
            }
            addresses.append(batch)
        
        # except:
        #     return Response({'error': 'Could not create addresses'}, status=HTTP_200_OK)
            


            if speed < 50: # ~40mph
                status = 'FF0000' # bad
            elif speed < 65: # ~40mph
                status = 'FF4081' # bad
            elif speed < 80: # ~50mph
                status = 'FF8000' #'poor'
            elif speed < 95: # ~60mph
                status = 'FFFF00' #'ok'
            elif speed < 110: # ~70mph
                status = '80FF00' #'good'
            else: # ~80mph
                status = '0A5D00' #'Excellent'

        # except:
            # return Response({'error': 'Could not fetch details from google'}, status=HTTP_200_OK)

 
    return Response({'response': batch}, status=HTTP_200_OK)

@api_view(['GET', 'POST'])
def bulk_segments_upload(request):
    if request.method == 'POST':
        routes = []
        for obj in request.data:
            routes.append(Route(route=obj.get("ROUTE")))

        Route.objects.bulk_create(routes, ignore_conflicts=True)

        # 1. Save segments
        addresses = []
        new_segments = []
        for obj in request.data:
            batch = {
                # 'route': obj.get("ROUTE"),
                'code': obj.get("SEGMENT_CODE"),
                'start_lat': json.dumps(obj.get("NORTHINGS")),
                'start_lng': json.dumps(obj.get("EASTINGS")),
                'end_lat': json.dumps(obj.get("NORTHINGS2")),
                'end_lng': json.dumps(obj.get("EASTINGS2")),
                'start_name': obj.get("START_NAME"),
                'end_name': obj.get("END_NAME"),
                # 'name': obj.get("SEGMENT_NAME"),
                # 'state': obj.get("STATE"),
            }
            addresses.append(batch)

            if json.dumps(obj.get("SEGMENT_NAME")) != 'null' and json.dumps(obj.get("STATE")) != 'null':
                new_segments.append(Segment(
                    code = obj.get("SEGMENT_CODE"),
                    name = obj.get("SEGMENT_NAME"),
                    state = obj.get("STATE"),
                    route = Route.objects.get(route=obj.get("ROUTE"))
                ))
            else:
                new_segments.append(Segment(
                    code = obj.get("SEGMENT_CODE"),
                    name = 'NO NAME',
                    state = 'NO STATE',
                    route = Route.objects.get(route=obj.get("ROUTE"))
                ))

        Segment.objects.bulk_create(new_segments, ignore_conflicts=True)

    google_addresses = []
    segments = []
    for point in addresses:
        # try:
            # 2. Fetch segment parameters from Google
            key = config('GOOGLE_ROUTES_API_KEY')
            url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=' + point['start_lat'] + '%2C' + point['start_lng'] + '&destinations=' + point['end_lat'] + '%2C' + point['end_lng'] + '&key=' + key

            # for multiple destintions (or possibly waypoints)
            # url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=6.45935%2C3.39926&destinations=6.65081%2C3.39157%7C6.83191%2C3.45898%7C6.96165%2C3.65673%7C6.45935%2C3.39926&key=AIzaSyD-mKszUKKRlSBlc8u9Tb8zj7UslWpDxB4"
            # - multiple destinations (waypoints)
            # - departure time: "https://maps.googleapis.com/maps/api/distancematrix/json?origins=Boston%2CMA%7CCharlestown%2CMA&destinations=Lexington%2CMA%7CConcord%2CMA&departure_time=now&key=YOUR_API_KEY"


            payload={}
            header = {}  

            response = requests.get(url, data=payload, headers=header).json()

            # 3. Save addresses2
            start_point = Address(
                address = response['origin_addresses'][0],
                lat = point['start_lat'],
                lng = point['start_lng'],
                name = point['start_name'],
            )
            google_addresses.append(start_point)

            end_point = Address(
                address = response['destination_addresses'][0],
                lat = point['end_lat'],
                lng = point['end_lng'],
                name = point['end_name'],
            )
            google_addresses.append(end_point)

            # 4. Create segments with distance, speed, and time of travel
            try:
                distance = round(response['rows'][0]['elements'][0]['distance']['value']/1000, 1)
            except KeyError: # no response from Google
                distance = 0.0

            try:
                duration = round(response['rows'][0]['elements'][0]['duration']['value']/60, 1)
            except KeyError: # no response from Google
                duration = 0.0
         
            try:
                speed = round((distance / (duration / 60)), 1)
            except:
                speed = 0.0


            if speed < 1:
                status = '666699' # no response from Google
            elif speed < 40:
                status = 'FF0000' # werser
            elif speed < 50:
                status = 'FF5050' # bad
            elif speed < 60: #
                status = 'FF9966' # poor
            elif speed < 70: #
                status = 'FFFFCC' # manage
            elif speed < 80:
                status = '00CC00' #'ok'
            elif speed < 90:
                status = '339933' #'good'
            else:
                status = '006600' #'better'

            segments.append({
                'code': point['code'],
                'distance': distance,
                'travel_time': duration,
                'avg_speed': speed,
                'status': status,
                'start': response['origin_addresses'][0],
                'end': response['destination_addresses'][0]
            })
        # except:
            # return Response({'error': 'Could not fetch details from google'}, status=HTTP_200_OK)

    Address.objects.bulk_create(google_addresses, ignore_conflicts=True)

    i = 0
    segments_to_update = []
    for segment in segments:
        seg = Segment.objects.filter(code=segment['code']).first()
        seg.distance = segment['distance']
        seg.travel_time = segment['travel_time']
        seg.avg_speed = segment['avg_speed']
        seg.status = segment['status']
        seg.start_point = Address.objects.get(address=segment['start'])
        seg.end_point = Address.objects.filter(address=segment['end']).first()
        segments_to_update.append(seg)
        # seg.save()
        i+=2

    Segment.objects.bulk_update(segments_to_update, ['distance', 'travel_time', 'avg_speed', 'status', 'start_point', 'end_point'])
    return Response({'response': request.data}, status=HTTP_200_OK)

@api_view(['GET', 'POST'])
def update_address(request):
    if request.method == 'POST':
        addresses = []
        for obj in request.data:
            code = obj.get("SEGMENT_CODE")
            start_lat = obj.get("NORTHINGS")
            start_lng = obj.get("EASTINGS")
            end_lat = obj.get("NORTHINGS2")
            end_lng = obj.get("EASTINGS2")
            # start_lat = json.dumps(obj.get("NORTHINGS"))
            # start_lng = json.dumps(obj.get("EASTINGS"))
            # end_lat = json.dumps(obj.get("NORTHINGS2"))
            # end_lng = json.dumps(obj.get("EASTINGS2"))

            for obj in request.data:
                # try:
                    segment = Segment.objects.get(code=code)
                    segment.start_point = Address.objects.filter(lat=start_lat, lng=start_lng)[:1]
                    segment.end_point = Address.objects.filter(lat=end_lat, lng=end_lng).first()
                    addresses.append(segment)
                    print(segment.start_point)
                # except:

        # Segment.objects.bulk_update(addresses, ['start_point', 'end_point'])
    return Response({'response': 'addresses updated'}, status=HTTP_200_OK)

@api_view(['GET', 'POST'])
def update_code(request):
    segments = Segment.objects.all()
    serializer = SegmentSerializer(segments, many=True)
        
    if request.method == 'POST':
        segments = []
        for obj in request.data:
            code = obj.get("SEGMENT_CODE")
            segment = Segment.objects.filter(code=code).first()
            segment.code = obj.get("NEW_CODE")
            segments.append(segment)

        Segment.objects.bulk_update(segments, ['code'])
    return Response({'response': serializer.data}, status=HTTP_200_OK)

@api_view(['GET', 'POST'])
def update_name(request):
    segments = Segment.objects.all()
    serializer = SegmentSerializer(segments, many=True)
        
    if request.method == 'POST':
        segments = []
        for obj in request.data:
            code = obj.get("SEGMENT_CODE")
            segment = Segment.objects.filter(code=code).first()
            segment.name = obj.get("NEW_SEGMENT_NAME")
            segments.append(segment)

        Segment.objects.bulk_update(segments, ['name'])
    return Response({'response': serializer.data}, status=HTTP_200_OK)

@api_view(['GET', 'POST'])
def update_state(request):
    segments = Segment.objects.all()
    serializer = SegmentSerializer(segments, many=True)
        
    if request.method == 'POST':
        segments = []
        for obj in request.data:
            code = obj.get("SEGMENT_CODE")
            segment = Segment.objects.filter(code=code).first()
            segment.state = obj.get("NEW_STATE")
            segments.append(segment)

        Segment.objects.bulk_update(segments, ['state'])
    return Response({'response': serializer.data}, status=HTTP_200_OK)