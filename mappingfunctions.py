import json
from geojson import FeatureCollection
from pprint import pprint
from geofunctions import find_distance



def make_feature_coll(parks):
    """"""

    geojson_parks = FeatureCollection([park.create_geojson_object() for park in parks])

    return json.dumps(geojson_parks)
    

def find_close_parks(origin, time, routing, parks):
    """Create a dictionary with park objects that correspond to the distance radius heuristic.

    Calculate the straight-line distance from the origin to each park location.
    If the distance is within the bounding box heuristic, then add the park ID
    and park object to the close_parks dictionary.
    """

    close_parks = {} # KEY park_id : VALUE park object

    for park in parks:
        dist = find_distance((origin.latitude, origin.longitude), (park.latitude, park.longitude))
        if dist < find_appx_dist(time, routing):
            close_parks[park.park_id] = park

    return close_parks
    # {32: <POPOS park_id: 32, address: 600 California St>, 33: <POPOS park_id: 33, address: 845 Market St>, ETC


def find_appx_dist(time, routing):
    """Approximate distance corresponding to bounding radius heuristic based on average routing speeds."""

    if routing == 'walking':
        appx_dist = int(time) * 0.06  # Average walking pace of 4 mph

        return appx_dist


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