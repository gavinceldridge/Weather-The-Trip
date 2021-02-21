it('should extract the minutes and hours from a google maps step duration', function () {
    expect(extractHoursMinutes("32 mins")).toEqual([32, 0]);
    expect(extractHoursMinutes("6 hours 12 mins")).toEqual([12, 6]);
});

it('should format a date time object to format to the weatherbit format ([4]-[2]-[2]-T[2]:[2]:[2])', function(){
    expect(formatDateForWeatherBit(new Date('February 18, 2021 05:24:00'))).toEqual("2021-02-18T13:24:00")
});

//NOT WORKING: needs JQuery
// it('should update the current #current-label to the input string', function(){
//     update_current_label();
//     expect(document.querySelector('#current-label').innerText).toEqual('new label');
// });

//NOT WORKING: needs to have access to python server api
// it('should output weather results upon submitting an origin and destination', function(){
//     document.querySelector('#origin').innerText = 'San Francisco';
//     document.querySelector('#destination').innerText = 'Santa Cruz';
//     const directionsService = new google.maps.DirectionsService();
//     const directionsRenderer = new google.maps.DirectionsRenderer();
//     calculateAndDisplayRoute(directionsService, directionsRenderer);
//     expect(document.querySelector('#weather-results').children.length).toBeGreaterThan(0);
// });