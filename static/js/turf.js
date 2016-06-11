"use strict";

map.on('load', function () {
    // Add park marker data from previously defined GeoJSON source.
    map.addSource("park_markers", park_markers_source);

    // Add turf data
    map.addSource('turf-data', {
        "type": "geojson",
        "data": grid
    });

    map.addLayer({
        "id": "turf-data",
        "type": "circle",
        "source": "turf-data",
        "paint": {
            "circle-color": "#f00",
            "circle-radius": 5
        }
    });

    grid.features.forEach(function (feature) {
        feature.properties["marker-color"] = "#6BC65F";
        feature.properties["marker-size"] = "small";
    });

// Create a bounding box ('envelope') around the markers
var enveloped = turf.envelope(park_markers);

// var resultFeatures = fc.features.concat(enveloped);

var result = { //put resulting envelope in geojson FeatureCollection format
    "type": "FeatureCollection",
    "features": [enveloped] 
};

// console.log([enveloped.geometry.coordinates[0][0][0],
//              enveloped.geometry.coordinates[0][0][1],
//              enveloped.geometry.coordinates[0][2][0],
//              enveloped.geometry.coordinates[0][2][1]]
//             );

// Use turf.point-grid [in order minX, minY, maxX, maxY]
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


// Build url for API call to request distance from origin to each point in the grid
// var distanceUrl = 'https://api.mapbox.com/distances/v1/mapbox/{{routing}}/?access_token=' + mapboxgl.accessToken;

// could initialize an empty variable
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

// In query string, add geometies as geojson (then don't have to deal with the polyline module)

$.ajax({
    type: 'GET',
    url: 'https://api.mapbox.com/directions/v5/mapbox/cycling/-122.42,37.78;-77.03,38.91?access_token=' + mapboxgl.accessToken,
    success: (r) => {
        console.log('I am a directions response:', r);
    },
    error: (e) => {
        console.error(e);
    }
});

