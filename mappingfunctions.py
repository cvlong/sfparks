import json
from geojson import FeatureCollection
from pprint import pprint
from geofunctions import find_distance



def make_feature_coll(parks, user_id):
    """Create a GeoJSON feature collection from a list of park objects."""

    geojson_parks = FeatureCollection([park.create_geojson_object(user_id) for park in parks])

    return json.dumps(geojson_parks)
    

def find_appx_dist(time, routing):
    """Approximate distance corresponding to bounding radius heuristic based on average routing speeds."""

    if routing == 'walking':
        appx_dist = int(time) * 0.06  # average walking pace of 4 mph
    elif routing == 'cycling':
        appx_dist = int(time) * 0.2  # average cycling pace of 12 mph

    return appx_dist


def find_close_parks(origin, time, routing, parks):
    """Create a dictionary with park objects that correspond to the distance radius heuristic.

    Calculate the straight-line distance from the origin to each park location to
    determine whether the distance is within the bounding box heuristic.
    """

    close_parks = {}

    for park in parks:
        dist = find_distance((origin.latitude, origin.longitude), (park.latitude, park.longitude))
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