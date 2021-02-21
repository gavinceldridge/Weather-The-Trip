$(document).ready(function () {

    //Map Plot Trash Items:
    $('.trash').click((evt)=>{
       
        input = evt.currentTarget.parentElement.children[0].id;//trash's corresponding input
        $(`#${input}`)[0].value='';
        $('#current-label')[0].innerText = input.charAt(0).toUpperCase() + input.slice(1);//set the current-label to the most recently deleted input
        
    });

    $('#search-form').submit(function (evt) {
        evt.preventDefault();
        locationSearch($('#location_input').get()[0].value);
    });
});