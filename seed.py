"""Utility file to seed SFparks database from parks & POPOS data in seed_data/"""

# from sqlalchemy import func

from model import connect_to_db, db #add Models
from server import app
# from datetime import datetime


def load_popos():
    """Load POPOS from u.popos into database."""

    print "POPOS"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate entries
    Popos.query.delete()

    # Read u.popos file and insert data
        #Iterate through data in "seed_data/u.popos"

        #popos = Popos(name=name,
        #              address=address, etc)

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
    