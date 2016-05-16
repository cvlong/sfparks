"""Models and database functions for SFparks project."""

from flask_sqlalchemy import SQLAlchemy
# from geojson import Point
from datetime import datetime


# Connect to PostgreSQL database through the Flask-SQLAlchemy helper library. Use
# 'session' object to commit, etc.
db = SQLAlchemy()


##############################################################################

#Model definitions

# TODO: Determine relationships b/w comments & users/parks. Set backref using foreign keys.

class Popos(db.Model):
    """Privately-Owned Public Open Space on SFparks website."""

    __tablename__ = "popos"

    popos_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    ptype = db.Column(db.String(100))


    def create_geojson_object(self):
        """Creates GeoJSON object for popos data."""
        
        geojson_obj = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [self.longitude, self.latitude]
            },
            "properties": {
                "name": self.name,
                "address": self.address,
                }
        }

        return geojson_obj


    @classmethod
    def get_park_type(cls, ptype):
        """Get all parks matching a certain park type."""

        return cls.query.filter_by(ptype=ptype).all()


    def __repr__(self):
        """Define how model displays."""

        return "<POPOS popos_id: {}, address: {}>".format(self.popos_id, self.address)


# class Park(db.Model):
#     """Aggregates IDs from POPOS, parks tables."""

    # __tablename__ = "parks"

    # TODO: SETUP ASSOCIATION TABLE


class User(db.Model):
    """User of SFparks website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    # TODO: add user's home, or saved starting location

    def __repr__(self):
        """Define how model displays."""

        return "<User user_id: {}, email: {}>".format(self.user_id, self.email)

    
# class Favorite(db.Model):
#     """Parks indicated as favorite by specific user."""

#     __tablename__ = "favorites"

#     fav_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     park_id = db.Column(db.Integer, db.ForeignKey('parks.park_id'), nullable=False)
#     #     # TODO: LINK TO PARKS ASSOCIATION TABLE
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)


# class Comment(db.Model):
#     """Comment from user on specific park."""

#     __tablename__ = "comments"

#     comment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     park_id = db.Column(db.Integer, db.ForeignKey('parks.park_id'), nullable=False)
#     # TODO: LINK TO PARKS ASSOCIATION TABLE

#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
#     logged_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
#     comment = db.Column(db.String(200), nullable=False)

#     def __repr__(self):
#         """Define how model displays."""

#         return "<Comment comment_id: {} by user user_id: {} for park park_id: {}>".format
#         (self.comment_id, self.user_id, park_id)




##############################################################################

def connect_to_db(app):
    """Connect database to Flask app."""

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sfparks'
    app.config['SQLALCHEMY_ECHO']=True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # Run module interactively to work with the database directly
    
    from server import app
    connect_to_db(app)
    print "Connected to DB."