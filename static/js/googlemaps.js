
let map;

function initMap(place = false) {
    const map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 37.817681, lng: -122.478371 },
        zoom: 7,
    });
    if (place) {
        const marker = new google.maps.Marker({
            position: place,
            map: map,
        });
    }
}
