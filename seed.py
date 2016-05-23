"""Utility file to seed SFparks database from external API requests and seed_data/"""

# from sqlalchemy import func

from model import connect_to_db, db, Popos, Posm #add Models
from server import app
import requests
from datetime import datetime


def load_popos():
    """Load Privately-Owned Public Open Space (POPOS) data from popos.csv into database."""

    print "Privately-Owned Public Open Space"

    # Delete all rows in table, so we're not creating duplicate entries
    # if we need to run this a second time
    Popos.query.delete()

    # Read popos.csv file and parse data
    for row in open("seed_data/popos.csv"):
        row = row.rstrip()

        name, address, latitude, longitude, subj, ptype = row.split(",")[1:7] 

        popos = Popos(name=name,
                      address=address,
                      latitude=float(latitude),
                      longitude=float(longitude),
                      ptype=ptype)

        # Add popos data to the db session
        db.session.add(popos)
        
    # Commit session to db
    db.session.commit()
    print "Committed to DB"


def load_posm():
    """Load Park & Open Space Map data from JSON into database."""

    print "Park & Open Spaces"

    # Delete all rows in table, so we're not creating duplicate entries
    # if we need to run this a second time
    Posm.query.delete()

    # Call API and parse data
    r = requests.get('https://data.sfgov.org/resource/94uf-amnx.json')
    parks = r.json()

    for item in parks:
        if item['parkservicearea'] != "Outside SF":
            name = item.get('parkname').title()
            ptype = item.get('parktype')
            acreage = item.get('acreage')
            zipcode = item.get('zipcode')
            try:
                coordinates = item.get('location_1').get('coordinates') # [-122.38450221, 37.73876792]
            except AttributeError:
               continue

        posm = Posm(name=name,
                    latitude=coordinates[1],
                    longitude=coordinates[0],
                    ptype=ptype,
                    acreage=acreage,
                    zipcode=zipcode)

        # Add posm data to the db session
        db.session.add(posm)

    # Commit session to db
    db.session.commit()
    print "Committed to DB"



##############################################################################

if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    # Import different types of data
    load_popos()
    load_posm()
    