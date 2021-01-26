let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 37.817681, lng: -122.478371 },
    zoom: 7,
  });
}