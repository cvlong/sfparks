"use strict";

// Disable map rotation using right click + drag or touch rotation gesture
map.dragRotate.disable();
map.touchZoomRotate.disableRotation();

// Create a popup info box on hover, but don't add it to the map yet
var popup = new mapboxgl.Popup({
    closeButton: false,
    closeOnClick: false
});

map.on('mousemove', function(e) {
    
    // Find all rendered features from the provided layers.
    var features = map.queryRenderedFeatures(e.point, { layers: ['popos_markers','posm_markers', 'fav-markers', 'park_markers'] });
    
    // Indicate that the symbols are clickable by changing the cursor style to
    // 'pointer' as a UI indicator
    map.getCanvas().style.cursor = (features.length) ? 'pointer' : '';

    if (!features.length) {
        popup.remove();
        return;
    }

    // Populate the popup and set its coordinates based on the feature found.
    var feature = features[0];
    
    // Set the HTML string using attributes from each layer's features. Assign a
    // unique ID to each 'favorite' button for executing Ajax calls. Pull data
    // from the favorite attribute on the initial geoJSON object, and assign the
    // class based on whether it's favorited or not; use that property to determine
    // the button class in the popup.

    // if (feature.properties.routing_mins === 'null') {
    //     var htmlString = "<div><h5>" + feature.properties.name + "</h5><button id=" +
    //         feature.properties.id + " class=" + feature.properties.favorite +
    //         " onclick='updateFavorite(" + feature.properties.id +
    //         ")'>&#x2605; Favorite</button></div>";
    // } else {
    //     var htmlString = "<div><h5>" + feature.properties.name + "</h5>" + 
    //         feature.properties.routing_mins + " minutes " + routing + "</p><button id=" +
    //         feature.properties.id + " class=" + feature.properties.favorite +
    //         " onclick='updateFavorite(" + feature.properties.id +
    //         ")'>&#x2605; Favorite</button></div>";
    // }


    if (feature.properties.routing_mins === 'null') {
        var htmlString = "<div><h5>" + feature.properties.name + "</h5><button id=" +
            feature.properties.id + " class=" + feature.properties.favorite +
            " onclick='updateFavorite(" + feature.properties.id +
            ")'>&#x2605; Favorite</button></div>";
    } else {
        var htmlString = "<div><h5>" + feature.properties.name + 
            "</h5><img class='mapboxgl-popup-img' src=" + feature.properties.img_url +
            "><span class='mapboxgl-popup-span'>" + feature.properties.routing_mins + " minutes " + routing + "</span></p><button id=" +
            feature.properties.id + " class=" + feature.properties.favorite +
            " onclick='updateFavorite(" + feature.properties.id +
            ")'>&#x2605; Favorite</button></div>";
    }


    popup.setLngLat(feature.geometry.coordinates)
        .setHTML(htmlString)
        .addTo(map);
});

function getIndexFromID(id) {
    return park_markers.features.filter(function(park)
        {return park.properties.id == id})[0]
}

// On click, update the favorite class dynamically and send an Ajax request
// to the server to update the database. Also, overwrite the geoJSON object so
// the features.properties.favorites is updated next time a popup is made.

function updateFavorite(id) {
    var parkGeo = getIndexFromID(id)
    if (($('#' + id).attr('class')) === 'not_favorite') {
        $('#' + id).attr('class', 'favorite'); // add .favorite class
        parkGeo.properties.favorite = 'favorite'; // update the geojson
        map.getSource('park_markers').setData(park_markers); // reset the new geojson data as the map source
        $.post('/update-favorite.json', {'id': id, 'class': 'favorite'}, favoriteSuccess); // send ajax request to server to update the database
    } else {
        $('#' + id).attr('class', 'not_favorite');
        parkGeo.properties.favorite = 'not_favorite';
        map.getSource('park_markers').setData(park_markers);
        $.post('/update-favorite.json', {'id': id, 'class': 'not_favorite'}, favoriteSuccess);
    }
}

function favoriteSuccess(result) {
    console.log(result.status);
}


function getDirections(id) {
    var parkGeo = getIndexFromID(id)
    console.log(parkGeo.geometry.coordinates)
    $.post('/directions.json', JSON.stringify({'coords': parkGeo.geometry.coordinates}), directionsSuccess); 
}

function directionsSuccess(result) {
    console.log(result.status);    
}
