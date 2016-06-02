import json
from collections import namedtuple
from pprint import pprint
from geopy.distance import vincenty
from geofunctions import geocode_location


def format_origin(origin):
    """Format origin input to be an instance of a named tuple."""
    
    if ',' in origin:
        coords = origin.split(',')

        Latlng = namedtuple('Latlng', 'latitude longitude')
        origin = Latlng(float(coords[0]), float(coords[1]))

    else:
        origin = geocode_location(origin)
        
    return origin


def find_appx_dist(time, routing):
    """Approximate distance corresponding to bounding radius heuristic based on average routing speeds."""

    if routing == 'walking':
        appx_dist = int(time) * 0.06  # average walking pace of 4 mph
    elif routing == 'cycling':
        appx_dist = int(time) * 0.2  # average cycling pace of 12 mph
    else:
        raise Exception("That routing profile does not exist.")

    return appx_dist


def find_close_parks(origin, time, routing, parks):
    """Create a dictionary with park objects corresponding to a distance radius heuristic.

    Use Vincenty's solution to the inverse geodetic problem to find straight-line
    distance from the origin to each park location and determine whether the
    distance is within the bounding box heuristic.
    """

    close_parks = {}

    for park in parks:
        dist = vincenty((origin.latitude, origin.longitude),
                        (park.latitude, park.longitude)).miles
        if dist < find_appx_dist(time, routing):
            close_parks[park.name] = park

    return close_parks


def add_routing_time(geojson_destinations, routing_times):
    """Add routing time (in seconds) to each GeoJSON objects' properties."""
    
    if len(geojson_destinations) == len(routing_times):

        for geojson_obj in geojson_destinations:
            geojson_obj['properties']['routing_time'] = routing_times.pop(0)

    else:
        pass
        # TODO: throw an error

    # pprint(geojson_destinations)

    return geojson_destinations

# --

#     for routing in geojson_destinations:
#         ['properties']['routing_time']

# def round_of_rating(number):
#     """Round a number to the closest half integer.
#     >>> round_of_rating(1.3)
#     1.5
#     >>> round_of_rating(2.6)
#     2.5
#     >>> round_of_rating(3.0)
#     3.0
#     >>> round_of_rating(4.1)
#     4.0"""

#     return round(number * 2) / 2
#     