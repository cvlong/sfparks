"""SFparks."""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import db, connect_to_db, User, Popos

# from geocoding import [FUNCTION NAMES]

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



@app.route('/query')
def query_parks():
    """"""
    # Query for park objects
    parks = Popos.query.all()
    print parks
    
    origins_list = []
    
    # 
    for item in parks:
        origins_list.append(create_geojson_object(item))
        print origins_list

    # Query and get the parks
    # Get back LIST of park objects
    # Then loop thourgh that LIST
    # And add geojson_iobjs to another list, or something else

    

@app.route('/login', methods=['POST', 'GET'])
def login():
    """Show login form."""

    return render_template('login.html')


@app.route('/process-login', methods=['POST'])
def process_login():
    """Log in existing users; adds new users to database along with password."""

    # Pull data from form
    email = request.form.get("email")
    password = request.form.get("password")

    # select the user from the database who has the given email (if any)
    user = User.query.filter_by(email=email).first()

    if user == None:
        # instantiate a user object with the information provided
        user = User(email=email, password=password)
        
        # add user to session and commit to database
        db.session.add(user)
        db.session.commit()

        # set a cookie identifying the user; return to homepage
        session['user_id'] = user.user_id
        
        flash("You're logged in.")
        return redirect('/')
    
    else:
        # check to see if password is correct
        if password == user.password:
            # set a cookie identifying the user; return to homepage
            session['user_id'] = user.user_id
            
            flash("You're logged in.")
            return redirect('/')
        
        else:  # if password does not match database
            # flash message, stay on page
            
            flash('Your password did not match. Please enter your information again.')
            return redirect('/login')


@app.route('/logout', methods=['POST'])
def process_logout():
    """Log user out."""

    # remove user id from session
    del session['user_id']
    
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