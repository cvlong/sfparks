"""SFparks."""

from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from geojson import Feature, Point
from model import db, connect_to_db, User, Popos, Posm
from geofunctions import geocode_location, reverse_coord, get_routing_times, geojson_origin_object
from mappingfunctions import find_close_parks, make_geojson_destinations, add_routing_time


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABCDEF"

# Raise an error for undefined variables in Jinja2
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage; render SF parks."""

    popos = Popos.query.all()
    posm = Posm.query.all()

    return render_template('homepage.html',
                            popos=popos,
                            posm=posm)


@app.route('/query', methods=['GET'])
def query_parks():
    """Return results from users' query based on origin location, time, and routing profile."""
    
    origin = request.args.get('origin')
    routing_time = request.args.get('routing_time')
    routing_profile = 'walking' # hardcoding this for now; TODO: incorporate into query params

    # Geocode origin address input to lat/lng tuple
    geocoded_origin = geocode_location(origin)
        # (37.792458, -122.395709)

    # Get all park objects in database
    parks = Popos.query.all()

    # Instantiate a dictionary containing park objects within bounding radius heuristic
    close_parks = find_close_parks(geocoded_origin, parks)

    # Instantiate a list of GeoJSON objects for parks in close_parks dictionary
    geojson_destinations = make_geojson_destinations(close_parks)

    # Convert geocoded_origin tuple to GeoJSON object; need to switch lat/lng to lng/lat tuple
    geojson_origin = Feature(geometry=Point(reverse_coord(geocoded_origin)))
        # Point(reverse_coord(geocoded_origin)) --> Feature(geometry=geojson_origin)

    # Instantiate a list of GeoJSON objects for the get_routing_times function
    routing_params = [geojson_origin] + geojson_destinations
    
    routing_times = get_routing_times(routing_params, routing_profile)[0][1:]
    # routing_times = list of time in seconds from origin to each destination in geojson_destinations


    markers = add_routing_time(geojson_destinations, routing_times)


        

    #Loop through geojson list
    #edit to add travel time parameter
    #new geojson list that contains travel time param



    return render_template('query.html',
                            origin=origin,
                            routing_time=routing_time,
                            close_parks=close_parks,
                            geojson_destinations=geojson_destinations,
                            routing_times=routing_times,
                            markers=markers)


    # print len(geojson_destinations) #8 - EIGHT destination items
    # print len(routing_time) #9 - ignore the first, which is origin

"""
[[0, 704.3, 638.5, 720.5, 687.9, 856.7, 582.1, 586.3, 617.2],
 



 index0     [704.3, 0, 744, 480, 16.4, 226, 261.6, 340.6, 433.6],
 index1     [638.5, 744, 0, 470.6, 738.7, 784.9, 562.3, 485.9, 348.5],
 index2     [720.5, 480, 470.6, 0, 496.4, 376.2, 298.3, 221.9, 178.4],
 index3     [687.9, 16.4, 738.7, 496.4, 0, 242.4, 278, 357, 450],
 index4     [856.6, 225.9, 784.8, 376.1, 242.3, 0, 356.9, 435.9, 492.6],
 index5     [582, 261.5, 562.2, 298.2, 277.9, 356.9, 0, 158.8, 251.8],
 index6     [586.2, 340.5, 485.8, 221.8, 356.9, 435.9, 158.8, 0, 175.4],
 index7     [617.2, 433.6, 348.5, 178.4, 450, 492.7, 251.9, 175.5, 0]]
"""



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