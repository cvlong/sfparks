"""Models and database functions for SFparks project."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# Connect to PostgreSQL database through the Flask-SQLAlchemy helper library. Use
# 'session' object to commit, etc.
db = SQLAlchemy()


##############################################################################

class Park(db.Model):
    """SF parks from POPOS and POSM data sources."""

    __tablename__ = "parks"

    park_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    park_type = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    popos = db.relationship('Popos', backref=db.backref('parks'))
    posm = db.relationship('Posm', backref=db.backref('parks'))

    def create_geojson_object(self):
        """Creates GeoJSON object for park data."""

        # if self.park_type == "popos":
        #     then marker-symbol==monument, etc.
        
        geojson_obj = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [self.longitude, self.latitude]
            },
            "properties": {
                "id": self.park_id,
                "type": self.park_type,
                "name": self.name,
                # "address": self.address, # FOR POPOS
                "marker-symbol": None,
                "routing_time": None,
                "favorite": None,
                }
        }

        return geojson_obj
    

    @classmethod
    def get_park_type(cls, park_type):
        """Get all parks matching a certain park type."""

        return cls.query.filter_by(park_type=park_type).all()


    def __repr__(self):
        """Define how model displays."""

        return "<park_id: {}, park_type: {}, name: {}>".format(self.park_id,
                                                               self.park_type,
                                                               self.name)


class Popos(db.Model):
    """Privately-Owned Public Open Space on SFparks website."""

    __tablename__ = "popos"

    primary = db.Column(db.Integer, autoincrement=True, primary_key=True)
    park_id = db.Column(db.Integer, db.ForeignKey('parks.park_id'), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    popos_type = db.Column(db.String(100))


    def __repr__(self):
        """Define how model displays."""

        return "<park_id: {}, address: {}>".format(self.park_id, self.address)


class Posm(db.Model):
    """Park & Open Space Map data on SFparks website."""

    __tablename__ = "posm"

    primary = db.Column(db.Integer, autoincrement=True, primary_key=True)
    park_id = db.Column(db.Integer, db.ForeignKey('parks.park_id'), nullable=False)
    posm_type = db.Column(db.String(100))
    acreage = db.Column(db.Float)
    zipcode = db.Column(db.Integer)


    def __repr__(self):
        """Define how model displays."""

        return "<park_id: {}, name: {}>".format(self.park_id, self.parks.name)


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

    
class Favorite(db.Model):
    """Parks indicated as favorite by specific user."""

    __tablename__ = "favorites"

    fav_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    park_id = db.Column(db.Integer, db.ForeignKey('parks.park_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    logged_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship('User', backref=db.backref('favorites'))

    park = db.relationship('Park', backref=db.backref('favorites'))


    def __repr__(self):
        """Define how model displays."""

        return "<User user_id: {}, park_id: {}, park_type: {}>".format(self.user, self.park_id, self.park.type)


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