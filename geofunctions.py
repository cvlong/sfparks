import os
from collections import namedtuple
from pprint import pprint
from mapbox import Geocoder, Distance, Directions
from model import db, connect_to_db, Popos, Posm


MB_ACCESS_TOKEN = os.environ['MAPBOX_ACCESS_TOKEN']
geocoder = Geocoder(access_token=MB_ACCESS_TOKEN)
service = Distance(access_token=MB_ACCESS_TOKEN)
service1 = Directions(access_token=MB_ACCESS_TOKEN)


def geocode_location(location):
    """Geocodes origin and returnes lng/lat in named tuple."""

    # Forward geocoding with proximity so results are biased toward given lng/lat
    response = geocoder.forward(location, lon=-122.431, lat=37.773)
    
    if response.status_code == 200:
        first = response.geojson()['features'][0]

        origin_lng = first['geometry']['coordinates'][0]
        origin_lat = first['geometry']['coordinates'][1]

        Latlng = namedtuple('Latlng', 'latitude longitude')
        origin = Latlng(origin_lat, origin_lng)

        return origin
        # Latlng(latitude=37.792458, longitude=-122.395709)

    else:
        pass
        # Add else condition

# print geocode_location("55 Main Street")


# def get_routing_time(origin, destinations, routing):
    # First argument = list w/ origin geojson object + geojson objects of all parks

def get_routing_times(routing_list, routing):
    """Use Mapbox Distance API to find routing time from origin to a list of features."""

    response = service.distances(routing_list, routing)

    if response.status_code == 200:
        # print response.headers['Content-Type']
        # 'application/json; charset=utf-8'

        # pprint(response.json()['durations'])
        # [[0, ..., ...], [..., 0, ...], [..., ..., 0]]

        return response.json()['durations'][0][1:]
        # [0][1:] returns the first line of the distance matrix, skipping the first
        # element (which has a value of 0).
    
    elif ['durations'] not in response.json():
        print response.json()['message']

        pass
        # TODO: if durations not in response.json print response.json
        # Log in log file; then say "an error has occurred please try again"

def get_directions(route, routing):
    """Use Mapbox Directions API to find routing directions between points."""

    response = service1.directions(routing)

    return response.json()


