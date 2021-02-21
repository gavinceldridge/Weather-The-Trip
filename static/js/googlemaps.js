// INFO FROM https://developers.google.com/maps/documentation/javascript/examples/places-searchbox#maps_places_searchbox-javascript 

// This example adds a search box to a map, using the Google Place Autocomplete
// feature. People can enter geographical searches. The search box will return a
// pick list containing a mix of places and predicted search terms.
// This example requires the Places library. Include the libraries=places
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places">

function initAutocomplete() {
    const directionsService = new google.maps.DirectionsService();
    const directionsRenderer = new google.maps.DirectionsRenderer();
    const map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 37.7749, lng: -122.4194 },
        zoom: 8,
        mapTypeId: "roadmap",
    });
    directionsRenderer.setMap(map);
    
    const onSubmitHandler = function (evt) {
        evt.preventDefault();
        calculateAndDisplayRoute(directionsService, directionsRenderer);
    };

    document.getElementById('submit-calculations').addEventListener('click', onSubmitHandler);


    // Create the search box and link it to the UI element.
    const input = document.getElementById("pac-input");
    const searchBox = new google.maps.places.SearchBox(input);
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
    // Bias the SearchBox results towards current map's viewport.
    map.addListener("bounds_changed", () => {
        searchBox.setBounds(map.getBounds());
    });
    let markers = [];
    // Listen for the event fired when the user selects a prediction and retrieve
    // more details for that place.
    searchBox.addListener("places_changed", () => {
        const places = searchBox.getPlaces();
        if (places.length == 0) {
            return;
        }
        // Clear out the old markers.
        markers.forEach((marker) => {
            marker.setMap(null);
        });
        markers = [];
        // For each place, get the icon, name and location.
        const bounds = new google.maps.LatLngBounds();
        places.forEach((place) => {
            if (!place.geometry) {
                console.log("Returned place contains no geometry");
                return;
            }
            const icon = {
                url: place.icon,
                size: new google.maps.Size(71, 71),
                origin: new google.maps.Point(0, 0),
                anchor: new google.maps.Point(17, 34),
                scaledSize: new google.maps.Size(25, 25),
            };
            // Create a marker for each place.
            markers.push(
                new google.maps.Marker({
                    map,
                    icon,
                    title: place.name,
                    position: place.geometry.location,
                })
            );


            if (place.geometry.viewport) {
                // Only geocodes have viewport.
                bounds.union(place.geometry.viewport);
            } else {
                bounds.extend(place.geometry.location);
            }
        });
        map.fitBounds(bounds);

        const formatted_address = searchBox.getPlaces()[0].formatted_address;        
        append_to_current_direction(formatted_address);
        
    });
}

function calculateAndDisplayRoute(directionsService, directionsRenderer) {
    directionsService.route(
        {
            origin: {
            query: document.getElementById("origin").value,
            },
            destination: {
            query: document.getElementById("destination").value,
            },
            travelMode: google.maps.TravelMode.DRIVING,
        },
        async function (response, status) {
            if (status === "OK") {
                directionsRenderer.setDirections(response);
                // console.log(response);
                const parsedResponse = parseResponseForLocations(response);
                response = await axios.post('/get-weather-report', parsedResponse);
                displayWeatherResults(response);            
            } else {
                window.alert("Directions request failed due to " + status);
            }
        }
    );
}

const update_current_label = ()=>{
    $inputDivs = $('.input-group-append').get()
    $inputDivs.forEach((element)=>{
        value = element.children[0].value;
        if(value === ''){
            $('#current-label')[0].innerText = element.children[0].placeholder;
            return;
        }
    });

}

const append_to_current_direction = (address)=>{
    $current = $('#current-label').get()[0].innerText.toLowerCase();
    // console.log($(`#${current}-input`))
    $(`#${$current}`).get()[0].value=address;
    update_current_label();
}

const formatDateForWeatherBit = (time)=>{
    //regex to match JS Date UTC time to the weather UTC time
    time = time.toISOString();
    time = time.match(/\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/g)[0];
    return time;
}

const extractHoursMinutes = (duration)=>{
    let minutes = 0;
    let hours = 0;

    if(duration.includes('hour')){
        hours = parseInt(duration.match(/(\d+)\shour/)[1]);
    }
    if(duration.includes('min')){
        minutes = parseInt(duration.match(/(\d+)\smin/)[1]);
    }
    return [minutes, hours];
}

const parseResponseForLocations = (response)=>{
    //NOTE: result's first 2 values are predetermined to be the end pt and start pt respectively
    const result = {times: {}, locations: {}};

    // let startTime = new Date().toISOString();
    let time = new Date();

    let endTime = new Date(time);
    let tripDuration = response.routes[0].legs[0].duration.text;
    [minutes, hours] = extractHoursMinutes(tripDuration);
    endTime.setHours(endTime.getHours() + hours);
    endTime.setMinutes(endTime.getMinutes() + minutes);
    
    // add start time/location to the result as result[1]
    result.times[0] = formatDateForWeatherBit(time).match(/(\d{4}-\d{2}-\d{2}T\d{2})/)[1] + ':00:00';
    result.locations[0] = `${response.routes[0].legs[0].steps[0].path[0].lat()}, ${response.routes[0].legs[0].steps[0].path[0].lng()}`;
    let resultCounter = 1;
    
    
    /*
    
    UPDATE TIME

    Then, for each hour, record a timestamp of where the driver *should* be
    and add to the array.
    
    
    */
    let miles = 0;
    let feet = 0;
    steps = response.routes[0].legs[0].steps;
    steps.forEach((step)=>{

        //update time
        const priorStepHour = time.getHours(); 
        const [minutes, hours] = extractHoursMinutes(step.duration.text);
        time.setMinutes(time.getMinutes() + minutes);
        time.setHours(time.getHours() + hours);
        let numberOfHoursOnStep;
        if(hours == 0){
            numberOfHoursOnStep = time.getHours() - priorStepHour;
        }else{
            let extra = 0;
            if(minutes + time.getMinutes() > 59){
                extra = 1;
            }
            numberOfHoursOnStep = hours + extra;
        }
        if(numberOfHoursOnStep > 0 && hours === 0){
            //     time = time.match(/\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/g)[0];

            const newResultTime = formatDateForWeatherBit(time).match(/(\d{4}-\d{2}-\d{2}T\d{2})/)[1] + ':00:00';
            result.times[resultCounter] = newResultTime;
            const lat = step.path[Math.floor(step.path.length/2)].lat();
            const lng = step.path[Math.floor(step.path.length/2)].lng();
            result.locations[resultCounter] = `${lat}, ${lng}`;
            resultCounter++;

        }else if(hours > 0){
            const stepPathTimeRatio = Math.floor((step.path.length-1)/numberOfHoursOnStep);
            for(let i = 0; i < numberOfHoursOnStep; i++){
                //get locations for step
                let timeAtIHour = new Date(time);
                timeAtIHour.setHours(time.getHours() - (numberOfHoursOnStep + i));
                const newResultTime = formatDateForWeatherBit(timeAtIHour).match(/(\d{4}-\d{2}-\d{2}T\d{2})/)[1] + ':00:00';
                result.times[resultCounter] = newResultTime;
                result.locations[resultCounter] = `${step.path[stepPathTimeRatio * i].lat()}, ${step.path[stepPathTimeRatio * i].lng()}`;
                resultCounter++;
            }
        }
    });

    //add end pt and time to the result as result[0]
    result.times[resultCounter] = formatDateForWeatherBit(endTime).match(/(\d{4}-\d{2}-\d{2}T\d{2})/)[1] + ':00:00';
    result.locations[resultCounter] = `${response.routes[0].legs[0].steps[response.routes[0].legs[0].steps.length-1].path[response.routes[0].legs[0].steps[response.routes[0].legs[0].steps.length-1].path.length-1].lat()}, ${response.routes[0].legs[0].steps[response.routes[0].legs[0].steps.length-1].path[response.routes[0].legs[0].steps[response.routes[0].legs[0].steps.length-1].path.length-1].lng()}`;
      
    return result;
}

const displayWeatherResults = (weatherResults)=>{
    const resultTable = document.querySelector('#weather-results');

    //reset results
    while(resultTable.children.length > 0){
        resultTable.removeChild(resultTable.children[0])
    }

    for(index in weatherResults.data.times){
        
        const tr = document.createElement('tr');
        
        const time = document.createElement('th');
        time.innerText = weatherResults.data.times[index];

        const location = document.createElement('td');
        location.innerText = weatherResults.data.locations[index];

        const description = document.createElement('td');
        description.innerText = weatherResults.data.results[index].substring(6, weatherResults.data.results[index].length)

        const code = document.createElement('td');
        code.innerText = weatherResults.data.results[index].substring(0, 4);

        tr.appendChild(time);
        tr.appendChild(location);
        tr.appendChild(description);
        tr.appendChild(code);
        resultTable.appendChild(tr);
    }

}
