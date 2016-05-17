from model import db, connect_to_db, Popos, Posm
from geofunctions import find_distance

# Instantiate an empty dictionary to record parks that correspond to the following distance radius heuristic
def find_close_parks(geocoded_origin, parks):
    close_parks = {} # KEY popos_id : VALUE popos object

    for park in parks:
        dist = find_distance(geocoded_origin, (park.latitude, park.longitude))
        if dist < .5: # later bring in dictionary that corresponds to bounding box heuristic
            close_parks[park.popos_id] = park

            # ?? how do I generalize the KEY - park ID

    return close_parks
    # {32: <POPOS popos_id: 32, address: 600 California St>, 33: <POPOS popos_id: 33, address: 845 Market St>, ETC


