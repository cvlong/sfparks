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
            time = routing_times.pop(0)
            geojson_obj['properties']['routing_time'] = time
            geojson_obj['properties']['routing_mins'] = format_routing_time(time)

    else:
        pass
        # TODO: throw an error

    return geojson_destinations


def format_routing_time(routing_time):
    """Convert API result from seconds to minutes; round result to closest half integer."""
    
    mins = routing_time / 60
    return round(mins * 2.0) / 2.0
