"""SFparks."""

import os
import sys
import logging

from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
import json
from pprint import pprint
from geojson import Feature, Point, FeatureCollection
from model import db, connect_to_db, Park, Popos, Posm, User, Favorite
from geofunctions import geocode_location, get_routing_times
from mappingfunctions import format_origin, find_close_parks, add_routing_time


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "abcdef")

# Additional logs for Heroku deployment
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

# Raise an error for undefined variables in Jinja2
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage; render all SF parks."""

    # If the user is logged in, add their favorites to the geojson park objects
    # rendered on page load.
    user_id = session.get('user')

    parks = Park.query.filter(~Park.name.contains('Playground'))

    geo_parks = FeatureCollection([park.create_geojson_object(user_id) for park in parks]) 
    # parks = json.dumps(geojson_parks)

    return render_template('homepage.html',
                            parks=geo_parks)


@app.route('/current-location.json', methods=['POST'])
def get_current_location():
    """Find user's current location from HTML5 Geolocation API."""

    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')

    return jsonify(status='success',
                   latitude=latitude,
                   longitude=longitude)


@app.route('/query', methods=['GET'])
def query_parks():
    """Return results from users' query based on search profile."""
    
    user_id = session.get('user')

    origin = request.args.get('origin')
    time = request.args.get('time')
    routing = request.args.get('routing')
    playgrounds = request.args.get('playgrounds')

    print "THIS IS THE ORIGIN WE ARE GETTING FROM THE GET REQUEST"
    print origin
    # Determine whether origin input is an address or lat/lng pair.
    origin = format_origin(origin)
    print "THIS IS THE ORIGIN THAT IS COMING FROM format_origin"
    print origin

    parks = Park.query.filter(~Park.name.contains('Playground'))

    # if playgrounds == None:
    # # Get parks that don't include "playground" in the name
    #     parks = Park.query.filter(~Park.name.contains('Playground'))
    # else:
    # # Get all park objects in database
    #     parks = Park.query.all()
    print "THIS IS THE ORIGIN THAT WE ARE USING TO CALL find_close_parks"
    print origin
    
    # Create a dictionary containing park objects within the bounding radius heuristic
    close_parks = find_close_parks(origin, time, routing, parks)

    # Create a list of GeoJSON objects for close parks
    geojson_destinations = [park.create_geojson_object(user_id)
                            for park
                            in close_parks.values()]
        # [{'geometry': {'type': 'Point', 'coordinates': [-122.40487, 37.79277]}, 'type': 'Feature', 'properties': {'name': u'600 California St', 'address': u'600 California St'}}, {'geometry': {'type': 'Point', 'coordinates': [-122.40652, 37.78473]}, 'type': 'Feature', 'properties': {'name': u'Westfield Sky Terrace (Wesfield Center Mall)', 'address': u'845 Market St'}},

    # Convert origin coordinates to GeoJSON object
    geojson_origin = Feature(geometry=Point((origin.longitude, origin.latitude)))
        # Point(origin) --> Feature(geometry=geojson_origin)

    # Create list of GeoJSON objects for get_routing_times argument
    routing_params = [geojson_origin] + geojson_destinations
        # TODO: try .insert to list (but don't want to change geojson_destinations to use later)
        # Will add_rounting_time() take these params as two separate lists?

    # Create distance matrix (routing time in seconds)
    routing_times = get_routing_times(routing_params, routing)

    # Create markers for the results of the user's query by adding each routing time to a park's GeoJSON properties
    all_markers = add_routing_time(geojson_destinations, routing_times)
        # print type(all_markers) #LIST
        # print type(all_markers[0]) #DICT

    markers = json.dumps(FeatureCollection(all_markers))
        # print type(markers) #STRING

    session['origin'] = [origin.longitude, origin.latitude]
    session['routing'] = routing

    return render_template('query.html',
                            origin=origin,
                            time=time,
                            routing=routing,
                            geojson_origin=geojson_origin,
                            geojson_destinations=geojson_destinations,
                            all_markers=all_markers,
                            markers=markers)


@app.route('/update-favorite.json', methods=['POST'])
def update_favorites():
    """Handle adding/removing favorite parks by the popup favorite button.

    If the user is logged in, add or remove favorites in the database. Otherwise,
    add or remove favorites in the session.
    """

    park_id = request.form.get('id')
    class_id = request.form.get('class')

    class_value = {
        'favorite': True,
        'not_favorite': False
    }
    
    user = session.get('user')
    
    if user:
        # First check whether user has favorited park before.
        favorited = Favorite.query.filter(Favorite.fav_park_id == park_id,
                                          Favorite.fav_user_id == user).first()
        
        if favorited:
            # print "This park is in the favorites db", favorited.fav_park_id
            # Unfavorite park by setting favorite property to False in the db.
            favorited.favorite = class_value[class_id]
            
            # print "If False, removing this park from favorites db. If True, adding to favorites db", favorited.favorite
            
            db.session.add(favorited)
            db.session.commit()

            return jsonify(status='successfully changed favorite')

        else:
            # Instantiate a favorite object with the information provided.
            favorite = Favorite(fav_park_id=park_id, 
                                fav_user_id=user)
            # print "This park is being added to user's favorites", favorite.fav_park_id

            db.session.add(favorite)
            db.session.commit()

            return jsonify(status='successfully added favorite')

    else:
        pass
        # TODO: if there's no session user, add favorites to session so they're
        # temporarily saved

    # return jsonify(status='successfully changed favorite')


@app.route('/favorites')
def return_favorites():
    """Display user's favorite parks."""

    user = session.get('user')
    
    if user:
        favorites = Favorite.query.filter(Favorite.fav_user_id == user).all()

    return render_template('favorites.html',
                            favorites=favorites)


@app.route('/directions.json', methods=['POST'])
def return_directions():
    """Display directions to a specific park."""

    route = session.get('origin')
    routing = session.get('routing')
    coords = request.get('coords')
    # print request.form
    #Use json.loads to read the string
    
    results = get_directions(route, routing)
    
    return jsonify(results)
    

@app.route('/login', methods=['POST'])
def login():
    """Show login form."""

    return render_template('login.html')


@app.route('/process-login', methods=['POST'])
def process_login():
    """Log in existing users and redirect to homepage."""

    email = request.form.get('email')
    password = request.form.get('password')

    # select the user from the database who has the given email (if any)
    user = User.query.filter(User.email==email).first()

    if user:
        # if user in database, check that password is correct
        if password == user.password:
            session['user'] = user.user_id
            
            flash("You're logged in.")
            return redirect('/')

        else:            
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
    new_user = User(email=email, 
                    password=password)
    
    # add user to db session and commit to db
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


@app.route('/about')
def show_about_page():
    """Show about page."""

    return render_template('about.html')


@app.route("/error")
def error():
    raise Exception("Error!")
    

##############################################################################

if __name__ == "__main__":
    # Set debug=True to invoke the DebugToolbarExtension
    # app.debug = True

    # connect_to_db(app, os.environ.get("DATABASE_URL"))
    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    PORT = int(os.environ.get("PORT", 5000))
    DEBUG = "NO_DEBUG" not in os.environ
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
