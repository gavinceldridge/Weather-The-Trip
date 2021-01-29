// INFO FROM https://www.youtube.com/watch?v=lSdM3yZkj1w
let map;

function initMap() {
    let mapOptions = {
        zoom:7,
        center: new google.maps.LatLng(37.817681, -122.478371)
    };
    map = new google.maps.Map(document.getElementById('map'), mapOptions);
    
    google.maps.event.addDomListener(window, 'load', initMap);
}

let defaultBounds = new google.maps.LanLngBounds(
    new google.maps.LatLng(-33.8902, 151.1759),
    new google.maps.LatLng(-33.8474, 151.2631));

let options = {bounds: defaultBounds}

let input = document.getElementById('pac-input');
map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
let autocomplete = new google.maps.places.Autocomplete(input, options);
