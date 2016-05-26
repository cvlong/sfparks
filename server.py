"""SFparks."""

from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
import json
from geojson import Feature, Point, FeatureCollection
from model import db, connect_to_db, User, Park, Popos, Posm
from geofunctions import geocode_location, get_routing_times
from mappingfunctions import find_close_parks, add_routing_time, make_feature_coll


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABCDEF"

# Raise an error for undefined variables in Jinja2
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage; render all SF parks."""

    parks = Park.query.all()
    parks = make_feature_coll(parks)

    return render_template('homepage.html',
                            parks=parks)


@app.route('/current-location.json', methods=['POST'])
def get_current_location():
    """Find user's current location based on browser data."""

    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')

    return jsonify(status='success', latitude=latitude, longitude=longitude)


# RETURN ALL OF THE MARKERS IN JSON
# MARKERS: KEY, VALUE: ALL MARKERS


@app.route('/query', methods=['GET'])
def query_parks():
    """Return results from users' query based on origin location, time profile, and routing profile."""
    
    origin = request.args.get('origin')
    time = request.args.get('time')
    routing = request.args.get('routing')

    # user_id = session.get('user_id')

    # # if the user is logged in, show favorites
    # if user_id:
    #     favorites = Favorite.query.filter_by(user_id=user_id).all()


    # Geocode user input; var origin is an instance of a named tuple
    origin = geocode_location(origin)

    # Get all park objects in database
    parks = Park.query.all()

    # Create a dictionary containing park objects within the bounding radius heuristic
    close_parks = find_close_parks(origin, time, routing, parks)

    # Create a list of GeoJSON objects for close parks
    geojson_destinations = [park.create_geojson_object() for park in close_parks.values()]
        # [{'geometry': {'type': 'Point', 'coordinates': [-122.40487, 37.79277]}, 'type': 'Feature', 'properties': {'name': u'600 California St', 'address': u'600 California St'}}, {'geometry': {'type': 'Point', 'coordinates': [-122.40652, 37.78473]}, 'type': 'Feature', 'properties': {'name': u'Westfield Sky Terrace (Wesfield Center Mall)', 'address': u'845 Market St'}},

    # Convert origin coordinates to GeoJSON object
    geojson_origin = Feature(geometry=Point((origin.longitude, origin.latitude)))
        # Point(reverse_coord(geocoded_origin)) --> Feature(geometry=geojson_origin)

    # Create list of GeoJSON objects for get_routing_times argument
    routing_params = [geojson_origin] + geojson_destinations
        # TODO: try .insert to list (but don't want to change geojson_destinations to use later)
        # Can add_rounting_times func take these params as two separate lists?
    
    routing_times = get_routing_times(routing_params, routing)
    # distance matrix (in seconds)

    # Create markers for the results of the user's query by adding each routing time to a park's GeoJSON properties
    markers = add_routing_time(geojson_destinations, routing_times)

    markers = json.dumps(FeatureCollection(markers))


    return render_template('query.html',
                            origin=origin,
                            time=time,
                            # close_parks=close_parks,
                            geojson_origin=geojson_origin,
                            geojson_destinations=geojson_destinations,
                            # routing_times=routing_times,
                            markers=markers)

    




#run server in interactive mode
# python -i server.py
# control C (just once)
# stops the script
# then can call functions

# @app.route('/favorites')
# # Add individual <user> to URL?
# # def show favorites:
#     """Display user's favorite parks."""

#     # user_id = session.get("user_id")
    
#     # if user_id:
#         # favorites = Favorite.query.filter_by(user_id=user_id).all()

#     # return render_template('favorites.html',
#     #                         favorites=favorites)


@app.route('/add-to-favorites.json', methods=['POST'])
def add_to_favorites():
    """Add park to user's favorites.

    If the user is logged in, add to favorite to the database. Otherwise,
    add the favorited park to the session.
    """

    park_id = request.form.get('id')
    park_type = request.form.get('type')

    print park_id
    print park_type

 
    user = session.get("user_id")
    """
    # if user is logged in, add park to the favorites db table
    if user:
        
        if park_type == "popos":
            # instantiate a favorite object with the information provided
            favorite = Favorite(popos_id=park_id, user_id=user_id)
        
        elif park_type == "posm":
            # instantiate a favorite object with the information provided
            favorite = Favorite(posm_id=park_id, user_id=user_id)

    # add favorite to db session and commit to database
    db.session.add(favorite)
    db.session.commit()

    print "Favorite committed to DB"
    # flash("") # No flash message for now because JS event handler changes the UI
    """
    # # see if user has favorited park before
    # Favorite.query.filter(Favorite.popos_id == park_id).first()

    
    # else:
        # session['user']

    return jsonify(status='successfully added favorite', id=park_id, type=park_type) #update this)


@app.route('/remove-from-favorites.json', methods=['POST'])
def remove_from_favorites():
    """Remove park from user's favorites.

    xxx
    """

    park_id = request.form.get('id')
    park_type = request.form.get('type')

    print park_id
    print park_type


    #REMOVE FROM DATABASE

    return jsonify(status='successfully removed favorite', id=park_id, type=park_type)



@app.route('/login', methods=['POST']) #note: took out 'GET' method
def login():
    """Show login form."""

    return render_template('login.html')


@app.route('/process-login', methods=['POST'])
def process_login():
    """Log in existing users and redirect to homepage."""

    email = request.form.get('email') # diff. from request.form('email')??
    password = request.form.get('password')

    # select the user from the database who has the given email (if any)
    user = User.query.filter(User.email==email).first()

    if user:
        # if user in database, check that password is correct
        if password == user.password:
            session['user'] = user.user_id
            
            flash("You're logged in.")
            return redirect('/')

        else:  # if password does not match database
            # flash message, stay on page
            
            flash('Your password is incorrect. Please enter your information again or register as a new user.')
            return redirect('/login')

    else:
        flash('Please register as a new user.')
        return redirect('register.html')


@app.route('/register', methods=['POST'])
def register():
    """Show registration form."""

    return render_template('register.html')


@app.route('/process-registration', methods=['POST'])
def process_registration():
    """Add new user to database and log them in."""

    email = request.form.get('email')
    password = request.form.get('password')

    # instantiate a user object with the information provided
    new_user = User(email=email, password=password)
    
    # add user to session and commit to database
    db.session.add(new_user)
    db.session.commit()

    # add user to the session; redirect to homepage
    session['user'] = new_user.user_id
    
    flash("You're logged in.")
    return redirect('/')


@app.route('/logout', methods=['POST'])
def logout():
    """Log user out."""

    # remove user_id from session
    del session['user']
    
    flash('You are now logged out.')
    return redirect('/')


##############################################################################

if __name__ == "__main__":
    # Set debug=True to invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()