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


    def create_geojson_object(self, user_id=None):
        """Creates GeoJSON object for park data."""
        
        geojson_obj = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [self.longitude,
                                self.latitude]
            },
            'properties': {
                'id': self.park_id,
                'type': self.park_type,
                'name': self.name,
                # 'address': None, set for POSM?
                'marker-symbol': None,
                'routing_time': None,
                'favorite': 'not_favorite'
                }
        }

        # If the user is logged in, update the GeoJSON object with their favorites.
        if user_id:
            fav_query_result = Favorite.query.filter(Favorite.fav_park_id == self.park_id,
                                                     Favorite.fav_user_id == user_id).first()
            if fav_query_result:
                geojson_obj['properties']['favorite'] = 'favorite'

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
    """Privately-Owned Public Open Space data on SFparks website."""

    __tablename__ = "popos"

    primary = db.Column(db.Integer, autoincrement=True, primary_key=True)
    park_id = db.Column(db.Integer, db.ForeignKey('parks.park_id'), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    popos_type = db.Column(db.String(100))

    park = db.relationship('Park', backref=db.backref('popos'))


    def __repr__(self):
        """Define how model displays."""

        return "<park_id: {}, address: {}>".format(self.park_id,
                                                   self.address)


class Posm(db.Model):
    """Park & Open Space Map data on SFparks website."""

    __tablename__ = "posm"

    primary = db.Column(db.Integer, autoincrement=True, primary_key=True)
    park_id = db.Column(db.Integer, db.ForeignKey('parks.park_id'), nullable=False)
    posm_type = db.Column(db.String(100))
    acreage = db.Column(db.Float)
    zipcode = db.Column(db.Integer)

    park = db.relationship('Park', backref=db.backref('posm'))


    def __repr__(self):
        """Define how model displays."""

        return "<park_id: {}, name: {}>".format(self.park_id,
                                                self.parks.name)


class User(db.Model):
    """User of SFparks website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    # TODO: add user's home, or saved starting location


    def __repr__(self):
        """Define how model displays."""

        return "<User user_id: {}, email: {}>".format(self.user_id,
                                                      self.email)

    
class Favorite(db.Model):
    """Parks indicated as favorite by specific user."""

    __tablename__ = "favorites"

    fav_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    favorite = db.Column(db.Boolean, default=False) 
        # change default to True?
    fav_park_id = db.Column(db.Integer, db.ForeignKey('parks.park_id'), nullable=False)
    fav_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    logged_at = db.Column(db.DateTime, default=datetime.utcnow)


    # Define realtionship to PARKS (one:many) // one PARK has many FAVORITES
    # So the *fav_park_id* column of the *favorites* table refers 
    # to the *park_id* column of the *parks* table:

    park = db.relationship('Park', backref=db.backref('favorites'))
    user = db.relationship('User', backref=db.backref('favorites'))


    def __repr__(self):
        """Define how model displays."""

        return "<Favorite: {}, User user_id: {}, Park park_id: {}>".format(self.favorite,
                                                                           self.fav_user_id,
                                                                           self.fav_park_id)


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