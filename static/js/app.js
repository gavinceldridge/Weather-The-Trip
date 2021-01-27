$(document).ready(function () {



    $('#search-form').submit(function (evt) {
        evt.preventDefault();
        locationSearch($('#location_input').get()[0].value);
    });

});