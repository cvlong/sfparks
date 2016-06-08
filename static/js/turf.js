"use strict";



map.on('load', function () {
    // Add park marker data from previously defined GeoJSON source.
    map.addSource("park_markers", park_markers_source);

    // // Add turf data.
    // map.addSource('turf-data', {
    //     "type": "geojson",
    //     "data": grid
    // });

    // // Add turf.
    // map.addLayer({
    //     "id": "turf-data",
    //     "type": "circle",
    //     "source": "turf-data",
    //     "paint": {
    //         "circle-color": "#f00",
    //         "circle-radius": 5
    //     }
    // });

    // grid.features.forEach(function (feature) {
    //     feature.properties["marker-color"] = "#6BC65F";
    //     feature.properties["marker-size"] = "small";
    // });





// Create a bounding box ('envelope') around the markers
var enveloped = turf.envelope(park_markers);

// var resultFeatures = fc.features.concat(enveloped);

var result = { //put the resulting envelope in a geojson format FeatureCollection
    "type": "FeatureCollection",
    "features": [enveloped] 
};

// console.log([enveloped.geometry.coordinates[0][0][0],
//              enveloped.geometry.coordinates[0][0][1],
//              enveloped.geometry.coordinates[0][2][0],
//              enveloped.geometry.coordinates[0][2][1]]
//             );

// Use turf.point-grid 
// has to be in order [minX, minY, maxX, maxY]
// TODO: Make this the extent of the entire city
var extent = [enveloped.geometry.coordinates[0][0][0],
             enveloped.geometry.coordinates[0][0][1],
             enveloped.geometry.coordinates[0][2][0],
             enveloped.geometry.coordinates[0][2][1]
             ];
             // EX: [-122.40379, 37.78618, -122.394668, 37.79374]
var cellWidth = 0.1; // in miles
var units = 'miles';

var grid = turf.pointGrid(extent, cellWidth, units);

// Iterate over this array to transform each object in the array from a feature
// to a string of two coordinates
    // var gridPoints = grid.features.map(function(feature) {
    //     return feature.geometry.coordinates.join(',')
    // }).join(';');

    // var fc = turf.featurecollection(gridPoints)

    // console.log(fc)

var coordArray = grid.features.map(function(point) {
    return point.geometry.coordinates;
});

console.log(coordArray)


// console.log(gridPoints)
// Returns an array of comma joined coordinates. Then join with semicolons to add
// to the string
// ["-122.41819743,37.78274031", "-122.41819743,37.783102025779755", etc.

                // $.post('/grid-distances.json', {'fc': fc}, gridDistanceSuccess);


                // var gridDistances

                // function gridDistanceSuccess(result) {
                //     // console.log(result.status);
                //     console.log(result)
                //     gridDistances = result;
                // }

                // console.log(gridDistances)



// Build url for API call to request distance from origin to each point in the grid
// var distanceUrl = 'https://api.mapbox.com/distances/v1/mapbox/{{routing}}/?access_token=' + mapboxgl.accessToken;

// couldinitialize an empty variable
var points;

$.ajax({
    type: 'POST',
    url: 'https://api.mapbox.com/distances/v1/mapbox/walking?access_token=' + mapboxgl.accessToken,
    data: JSON.stringify({
                coordinates: grid.features.slice(0,100).map(f => f.geometry.coordinates)
            }),
    processData: false,
    contentType: 'application/json',
    origin: 'http://localhost:8000',
    success: (r) => {
        console.log('I am a distances response:', r);
        // could make a functions createIsodistances and call that later on
    },
    error: (e) => {
        console.error(e);
    }
});

// .map(function(f) {return f.geometry.coordinates; })

//in query string, add geometies = geojson (then you don't have to deal with the polyline module)

$.ajax({
    type: 'GET',
    url: 'https://api.mapbox.com/directions/v5/mapbox/cycling/-122.42,37.78;-77.03,38.91?access_token=' + mapboxgl.accessToken,
    success: (r) => {
        console.log('I am a directions response:', r);
    },
    error: (e) => {
        console.error(e);
    }
})




// takes two waypoints, and uses that to make a directions requestuild string 
// /'coordstring'
// ' + 'mapbox.walking' + '/' + coords.map(function(c) { c[0] + ',' + c[1]; ' }).join(';')  
// #map iterates over the array and returns a version of it

// var coordstring = '';
// for (var i = 0; i < coords.length; i++) {
//     coordstring += coords[i][0] + coords[i][1]
// }

// distance API is a post request
// so look at jquery post request documentation to structure this
// .post()
// probably need to set header:
// type:post
// url:url, etc.
// content type - see example request





//build url to request distance to each point in the grid

//feature collection.features = array of features
//fc.features.map(function(feature) {return feature.geometry.coordinates.join(',')}
//iterating over this array. transforms each object in the array from a feature to a string of two coordinates
//mao over ffeatures since it's an array
//that will be an array of comma joined coordinates, then join with semicolons to add to the string

// still save the grid as the fc
// want to use the center coordinate, then add the descrinations
//so for objects in the fc (remember they'll be off by one) then add this as a property to each geojson feature


