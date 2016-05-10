"""Utility file to seed SFparks database from parks & POPOS data in seed_data/"""

# from sqlalchemy import func

from model import connect_to_db, db, Popos #add Models
from server import app
# from datetime import datetime


def load_popos():
    """Load POPOS from popos.csv into database."""

    print "POPOS"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate entries
    Popos.query.delete()

    # Read popos.csv file and parse data
    for row in open("seed_data/popos.csv"):
        row = row.rstrip()

        objectid, name, address, latitude, longitude, ptype = row.split(",")[:6] 

        popos = Popos(name=name,
                      address=address,
                      latitude=latitude,
                      longitude=longitude,
                      ptype=ptype)

        # Add popos to the db session
        db.session.add(popos)

    # Commit session to db
    db.session.commit()


def load_posm():
    """Load Park & Open Space Map from posm.csv into database."""

    print "Park & Open Spaces"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate entries
    Posm.query.delete()

    # Read posm.csv file and parse data
    for row in open("seed_data/posm.csv"):
        row = row.rstrip()

        name, ptype = row.split(",")[:2]
        location = row.split(",")[-1]

        location = location.split("(").rstrip(")")
        print location

        posm = Posm(name=name,
                    ptype=ptype)

        # Add popos to the db session
        db.session.add(popos)

    # Commit session to db
    db.session.commit()


##############################################################################

if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    # Import different types of data
    load_popos()
    