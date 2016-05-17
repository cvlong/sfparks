import os
from mapbox import Geocoder, Distance
from geopy.distance import vincenty
from pprint import pprint
from model import db, connect_to_db, Popos, Posm


MB_ACCESS_TOKEN = os.environ['MAPBOX_ACCESS_TOKEN']
geocoder = Geocoder(access_token=MB_ACCESS_TOKEN)
service = Distance(access_token=MB_ACCESS_TOKEN)

# Note: run 'source secrets.sh' before running 
# this file to set required environmental variables


def geocode_location(location):
    """Forward geocoding returns lng/lat for address."""

    # Forward geocoding with proximity so results are biased toward a given lng/lat
    response = geocoder.forward(location, lon=-122.431, lat=37.773)
    
    # print response.status_code
    # 200

    first = response.geojson()['features'][0]
        # print first['place_name'] # '55 Main St, San Francisco, California 94105, United States'
        # print first['geometry']['coordinates'] # [-122.395709, 37.792458]
    origin_lng = first['geometry']['coordinates'][0]
    origin_lat = first['geometry']['coordinates'][1]

    origin_coord = (origin_lat, origin_lng)
    return origin_coord
    # (37.792458 -122.395709)
    # need this tuple format for vincenty calculation in find_distance()

# geocode_location("55 Main Street")


def reverse_coord(coord):
    """Reverse lat/lng to lng/lat in tuple."""

    reversed_coord = (coord[1], coord[0])
    return reversed_coord
    # (-122.395709, 37.792458)

# reverse_coord((37.792458 -122.395709)


def find_distance(origin, destination):
    """Find straight-line distance between two points entered as lat/lng tuples."""

    return vincenty(origin, destination).miles


def geojson_origin_object(origin_lng, origin_lat):
    """Create GeoJSON object for origin location."""
    
    geojson_obj = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [origin_lng, origin_lat]
        },
        "properties": {
            "name": None,
            }
    }

    return geojson_origin_obj


# The input waypoints to the distance method are features,
# typically GeoJSON-like feature dictionaries
origin = {
    'type': 'Feature',
    'properties': {'name': '555'},
    'geometry': {
        'type': 'Point',
        'coordinates': [-122.7282, 45.5801]}}
destination = {
    'type': 'Feature',
    'properties': {'name': '555 Mission St'},
    'geometry': {
        'type': 'Point',
        'coordinates': [-122.39891, 37.7884]}}

# Write function to trasform database info > name, coordinates in GeoJSON dictionary
# geojson.io to check!

# Filter using turf before sending reuest


# def get_routing_time(origin, destinations, routing):
    # First argument = list w/ origin geojson object + geojson objects of all parks

def get_routing_times(routing_list, routing_profile):
    """Find routing time from origin to a list of features.

    The Mapbox Distance API optimizes travel between several waypoints,
    producing a "Distance Matrix" showing travel times between all waypoints.
    The routing_list is a list of GeoJSON point features for the origin plus
    each park destination.
    """

    # response = service.distances([origin, destinations], routing)
    response = service.distances(routing_list, routing_profile)
    
    print response.status_code
    # 200
    
    # print response.headers['Content-Type']
    # 'application/json; charset=utf-8'

    pprint(response.json()['durations'])
    # [[0, ..., ...], [..., 0, ...], [..., ..., 0]]

    return response.json()['durations']
