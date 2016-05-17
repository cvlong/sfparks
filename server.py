"""SFparks."""

from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from model import db, connect_to_db, User, Popos
from mappingfunc import geocode_location, reverse_coord, find_distance, get_routing_distance, origin_geojson_object
from geojson import Feature, Point


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABCDEF"

# Raise an error for undefined variables in Jinja2
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage; render SF parks."""

    parks = Popos.query.all()


    return render_template('homepage.html',
                            parks=parks)


@app.route('/query', methods=['GET'])
def query_parks():
    """Return results from users' query based on origin location and routing time."""
    
    origin = request.args.get('origin')
    routing_time = request.args.get('routing_time')
    routing_profile = 'walking' # hardcoding this for now; eventually incorporate into query params

    # Geocode address input on homepage to lat/lng tuple
    geocoded_origin = geocode_location(origin)
        # geocoded_origin = (37.792458, -122.395709)

    # Get all park objects in database
    parks = Popos.query.all()
        # [<POPOS popos_id: 1, address: 555 Mission St>, <POPOS popos_id: 2, address: 400 Howard St>, ETC

    # Instantiate an empty dictionary to record parks that correspond to the following distance radius heuristic
    close_parks = {} # KEY popos_id : VALUE popos object

    for park in parks:
        dist = find_distance(geocoded_origin, (park.latitude, park.longitude))
        if dist < .5: # later bring in dictionary that corresponds to bounding box heuristic
            close_parks[park.popos_id] = park

    print close_parks
        # {32: <POPOS popos_id: 32, address: 600 California St>, 33: <POPOS popos_id: 33, address: 845 Market St>, ETC

    # Instantiate an empty list to hold GeoJSON objects for parks in close_parks
    geojson_list = []

    # Unpack close_parks dict to append GeoJSON objects to geojson_list
    for park_id, park in close_parks.items():
        geojson_list.append(park.create_geojson_object())

    print geojson_list
        # [{'geometry': {'type': 'Point', 'coordinates': [-122.40487, 37.79277]}, 'type': 'Feature', 'properties': {'name': u'600 California St', 'address': u'600 California St'}}, {'geometry': {'type': 'Point', 'coordinates': [-122.40652, 37.78473]}, 'type': 'Feature', 'properties': {'name': u'Westfield Sky Terrace (Wesfield Center Mall)', 'address': u'845 Market St'}},


    # Convert geocoded_origin tuple to GeoJSON object; need to switch lat/lng to lng/lat tuple
    origin_geojson = Feature(geometry=Point(reverse_coord(geocoded_origin)))
        # Point(reverse_coord(geocoded_origin)) --> Feature(geometry=origin_geojson)

    routing_params = [origin_geojson] + geojson_list
    

    # get_routing_distance(origin, destinations, 'walking')
    routing_time = get_routing_distance(routing_params, 'walking')
    
    print len(geojson_list)
    print len(routing_distance)



    return render_template('query.html',
                            origin=origin,
                            routing_time=routing_time,
                            close_parks=close_parks,
                            geojson_list=geojson_list,
                            routing_distance=routing_distance)


"""
#run server in interactive mode
# python -i server.py
# control C (just once)
# stops the script
# then can call functions
"""


    # parks = Popos.query.all()
    # print parks
    
    # destination_list = []
    
    # for item in parks:
    #     geojson = item.create_geojson_object
    #     destination_list.append(geojson)
    #     print destination_list

    # return destination_list

    # Query and get the parks
    # Get back LIST of park objects
    # Then loop thourgh that LIST
    # And add geojson_objs to another list, or something else




@app.route('/login', methods=['POST']) #note: took out 'GET' method
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
        # check to see if password is correct
        if password == user.password:
            session['user'] = user.user_id
            
            flash("You're logged in.")
            return redirect('/')
        
        else:  # if password does not match database
            # flash message, stay on page
            
            flash('Your password is incorrect. Please enter your information again or register as a new user.')
            return redirect('/login')


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

    # remove user id from session
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