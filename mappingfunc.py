import os
from mapbox import Geocoder, Distance
from pprint import pprint
from model import db, connect_to_db, Popos
from geopy.distance import vincenty



MB_ACCESS_TOKEN = os.environ['MAPBOX_ACCESS_TOKEN']
geocoder = Geocoder(access_token=MB_ACCESS_TOKEN)
service = Distance(access_token=MB_ACCESS_TOKEN)

# Note: run 'source secrets.sh' before running 
# this file to set required environmental variables

def geocode_location(geocode_input):
    """Forward geocoding returns long/lat for location."""

    # Forward geocoding with proximity so results are biased toward a given long/lat
    response = geocoder.forward(geocode_input, lon=-122.431, lat=37.773)
    
    # print response.status_code
    # 200

    # print response.json()

    first = response.geojson()['features'][0]
    print first['place_name']
    # '55 Main St, San Francisco, California 94105, United States'
    print first['geometry']['coordinates']
    # [-122.395709, 37.792458]
    origin_lon = first['geometry']['coordinates'][0]
    origin_lat = first['geometry']['coordinates'][1]
    
    print origin_lon, origin_lat
    # -122.395709, 37.792458

    return (origin_lat, origin_lon)
    # (37.792458 -122.395709)
    # need this tuple format for vincenty calculation in find_distance()

geocode_location("55 Main Street")


def find_distance(origin, destination):
    """Find straight-line distance between two locations entered as tuples."""

    return vincenty(origin, destination).miles

# find_distance()


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
# First argument: fist of origin + all parks

def get_routing_directions(origin, destinations, routing):
    """Find directions with a list of features and the desired profile."""

    response = service.distances([origin, destination], routing)
    
    print response.status_code
    # 200
    
    print response.headers['Content-Type']
    # 'application/json; charset=utf-8'

    pprint(response.json()['durations'])
    # [[0, ..., ...], [..., 0, ...], [..., ..., 0]]

# get_routing_directions(origin, [destinations], 'walking')


