"""Utility file to seed SFparks database from external API requests and seed_data/"""

import requests
from datetime import datetime
from server import app
from model import connect_to_db, db, Park, Popos, Posm #add Models


def load_popos():
    """Load Privately-Owned Public Open Space (POPOS) data from popos.csv into database."""

    print "Privately-Owned Public Open Space"

    # Read popos.csv file and parse data
    for row in open("seed_data/popos.csv"):
        row = row.rstrip()

        name, address, latitude, longitude, subj, popos_type = row.split(",")[1:7]

        park = Park(park_type='popos',
                    name=name,
                    latitude=float(latitude),
                    longitude=float(longitude))

        # Add popos data to the parks db session & commit session to db
        db.session.add(park)
        db.session.commit()

        popos = Popos(park_id=park.park_id,
                      address=address,
                      popos_type=popos_type)

        # Add popos data to the popos db session & commit session to db
        db.session.add(popos)
        db.session.commit()
    
    print "Committed to DB"


def load_posm():
    """Load Park & Open Space Map data from JSON into database."""

    print "Park & Open Spaces"

    # Call API and parse data
    r = requests.get('https://data.sfgov.org/resource/94uf-amnx.json')
    parks = r.json()

    for item in parks:
        if item['parkservicearea'] != "Outside SF":
            name = item.get('parkname').title()
            posm_type = item.get('parktype')
            acreage = item.get('acreage')
            zipcode = item.get('zipcode')
            try:
                coordinates = item.get('location_1').get('coordinates') # [-122.38450221, 37.73876792]
            except AttributeError:
               continue

        park = Park(park_type='posm',
                    name=name,
                    latitude=coordinates[1],
                    longitude=coordinates[0])

        # Add posm data to the parks db session & commit session to db
        db.session.add(park)
        db.session.commit()

        posm = Posm(park_id=park.park_id,
                    posm_type=posm_type,
                    acreage=acreage,
                    zipcode=zipcode)

        # Add posm data to the posm db session & commit session to db
        db.session.add(posm)
        db.session.commit()
    
    print "Committed to DB"

##############################################################################

if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    # Import different types of data
    load_popos()
    load_posm()
    