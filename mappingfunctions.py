from pprint import pprint
from geofunctions import find_distance

dist_heuristic = {
    "5" : 0.3,
    "10" : 0.6,
    "15" : 1,
    "20" : 1.3,
    "30" : 2,
    "45" : 2.6,
}

def find_close_parks(geocoded_origin, parks):
    """Create a dictionary with park objects that correspond to the distance radius heuristic.

    Calculate the straight-line distance from the origin to each park location.
    If the distance is within the bounding box heuristic, then add the park ID
    and park object to the close_parks dictionary.
    """

    close_parks = {} # KEY park_id : VALUE park object

    for park in parks:
        dist = find_distance(geocoded_origin, (park.latitude, park.longitude))
        if dist < .5: # later bring in dictionary that corresponds to bounding box heuristic
            close_parks[park.park_id] = park

    return close_parks
    # {32: <POPOS park_id: 32, address: 600 California St>, 33: <POPOS park_id: 33, address: 845 Market St>, ETC

def make_geojson_destinations(close_parks):
    """Create a list with GeoJSON objects for parks in close_parks dictionary."""

    geojson_destinations = []

    # Unpack close_parks dict to append GeoJSON objects to geojson_destinations
    for park_id, park in close_parks.items():
        geojson_destinations.append(park.create_geojson_object())

    return geojson_destinations
    # [{'geometry': {'type': 'Point', 'coordinates': [-122.40487, 37.79277]}, 'type': 'Feature', 'properties': {'name': u'600 California St', 'address': u'600 California St'}}, {'geometry': {'type': 'Point', 'coordinates': [-122.40652, 37.78473]}, 'type': 'Feature', 'properties': {'name': u'Westfield Sky Terrace (Wesfield Center Mall)', 'address': u'845 Market St'}},


def add_routing_time(geojson_destinations, routing_times):
    """Adds routing time to GeoJSON object properties."""
    for geojson_obj in geojson_destinations:
        geojson_obj['properties']['routing_time'] = routing_times.pop(0)

    pprint(geojson_destinations)

    return geojson_destinations

     #  [{'geometry': {'coordinates': [-122.40487, 37.79277], 'type': 'Point'},
     #  'properties': {'address': u'600 California St',
     #                 'name': u'600 California St',
     #                 'routing_time': 704.3},
     #  'type': 'Feature'},
     # {'geometry': {'coordinates': [-122.40652, 37.78473], 'type': 'Point'},
     #  'properties': {'address': u'845 Market St',
     #                 'name': u'Westfield Sky Terrace (Wesfield Center Mall)',
     #                 'routing_time': 638.5},
     #  'type': 'Feature'},
