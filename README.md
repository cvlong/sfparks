# SFparks

Need to take a break outdoors? SFparks is an interactive web application that displays parks and public open spaces based on a user’s preferences. This app takes into account how long a user will allot for travel and whether they’re walking or cycling in order to identify parks and open spaces that match their routing profile. Users can also log in to keep track of their favorite parks and save their search results.

https://sfparks.herokuapp.com/

## Table of Contents
- [Technologies used](#tech)
- [Overview](#overview)
- [How it works](#how)
- [Next steps](#next)
- [Author](#author)

### <a name="tech"></a>Technologies used
- Python
- PostgreSQL
- SQLAlchemy
- Flask
- Jinja
- Javascript
- jQuery
- AJAX
- Bootstrap
- HTML
- CSS
- Yelp API
- Turf.js
- Mapbox GL JS

Dependencies are listed in requirements.txt

### <a name="overview"></a>Overview
SFparks uses HTML5, CSS, and Javascript on the client side and leverages the Mapbox API for data visualization. All interactions with the back end are managed through AJAX for a better user experience. Park data is stored in a PostgreSQL database, which has been seeded with open source data available on SF OpenData, including [San Francisco Parks and Open Spaces](https://data.sfgov.org/Culture-and-Recreation/Park-and-Open-Space-Map/4udc-s3pr) and downtown's [Privately Owned Public Open Spaces](https://data.sfgov.org/Geographic-Locations-and-Boundaries/Privately-Owned-Public-Open-Space-POPOS-and-Public/55um-v9vc) data. The app runs on Flask, a Python web framework based on the Werkzeug module and Jinja2 template engine, and uses SQLAlchemy as the ORM.

### <a name="how"></a>How it works
When SFparks first loads, the homepage displays all parks and open spaces queried from the database. If a user is logged in, their favorite parks will also be mapped.

![Homepage](/static/img/homepage.png)

#### Geocoding & searching
The user provides a starting location and routing profile for the search query.

For a starting location, the user can input an address which is translated to latitude/longitude coordinates using the Mapbox geocoding API or chose to use their current location, which is filled in to the search form using the HTML5 geolocation API. The user also specifies timing and routing conditions, which are posted to the server with their starting coordinates.

![Search](/static/img/search.png)

#### Server-side logic
To make the final distances API call less 'expensive', the database is first queried for parks that fall within a bounding box-based heuristic based on average walking and cycling speeds. The server then calls a method on these Park objects to create GeoJSON objects for each park that meets this criteria. Finally the Mapbox distance API is used to calculate the travel time to each of those parks based on the user’s specified routing profile. The GeoJSON objects are updated with this value and loaded onto a new page that renders a new map layer for parks that are within the travel time + routing profile determined by the user.

![Search](/static/img/results.png)

#### Adding favorites
If a user is logged in, they can access or update their favorite parks through the pop-up window, which appears when hovering over a park marker on the map. To add or change a favorite, a user can toggle the favorite button; this event will:
- Dynamically update the button’s CSS class as a UI indicator that the state has changed,
- Send an AJAX request serialized as JSON to the server to update the database (changing the park’s 'favorite' value for the specific user),
- Rewrite GeoJSON object’s properties, and re-renders the layer onto the map with this updated data source (so the next time the user hovers over the park, the pop-up shows the correct state of the user’s favorite).

### <a name="next"></a>Next steps & improvements
- Continue to add testing.
- Add Shapefile data using PostGIS (geospatial database) to store and serve spatial data dynamically; use the GeoAlchemy ORM.
- Incorporate functionality based on search parameters for two users (query for intersecting parks based off of two different routing profiles).
- Make the structure of my code more object oriented by break functions into classes.

### <a name="author"></a>Author
Christina Long is a Software Engineer in San Francisco, CA.  
[Email](mailto:cvlong@gmail.com) | [LinkedIn](https://www.linkedin.com/in/cvlong)