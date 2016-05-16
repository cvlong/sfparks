"""SFparks."""

from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from model import db, connect_to_db, User, Popos
from mappingfunc import get_routing_directions, find_distance


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



@app.route('/query', methods="GET")
def query_parks():
    """"""
    
    origin = request.args.get("origin")

    # routing_profile = 'walking'

    geocode_origin = (geocode_location(origin))
    print geocode_origin
    # (37.792458 -122.395709)

    # hardcoding origin for testing (lat, lon tuple)
    origin = (37.792458, -122.395709)

    parks = Popos.query.all()
    close_parks = {}

    for park in parks:
        dist = find_distance(origin, (park.latitude, park.longitude))
        if dist < .5: # later bring in dictionary that corresponds to bounding box heuristic
            close_parks[park.popos_id] = park, dist

    print close_parks

    return render_template('query.html',
                            close_parks=close_parks)

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
    # And add geojson_iobjs to another list, or something else




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
    user = User.query.filter_by(User.email=email).first()

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


@app.route('/register')
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


@app.route('/logout')
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