"""Models and database functions for SFparks project."""

from flask_sqlalchemy import SQLAlchemy

# Connect to PostgreSQL database through the Flask-SQLAlchemy helper library. Use
# 'session' object to commit, etc.
db = SQLAlchemy()


##############################################################################

#Model definitions

class Popos(db.Model):
    """Public Open Spaces on SFparks website."""

    __tablename__ = "popos"

    popos_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    ptype = db.Column(db.String(100))

    def __repr__(self):
        """Define how model displays."""

        return "<POPOS popos_id=%s address=%s>" % (self.popos_id, self.address)




        popos = Popos(


# class User(db.Model):
#     """User on SFparks website."""

#     __tablename__ = "users"

#     user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     email = db.Column(db.String(64), nullable=True)
#     password = db.Column(db.String(64), nullable=True)

#     def __repr__(self):
#         """Define how model displays."""

#         return "<User user_id=%s email=%s>" % (self.user_id, self.email)


##############################################################################

def connect_to_db(app):
    """Connect database to Flask app."""

    # Configure to use PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sfparks'
    app.config['SQLALCHEMY_ECHO']=True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # Run module interactively to work with the database directly
    
    from server import app
    connect_to_db(app)
    print "Connected to DB."