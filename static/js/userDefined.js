/**
 * Created by shivampatel on 3/21/17.
 */


function sendData()
{
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            var lat = position.coords.latitude;
            var lng = position.coords.longitude;
            console.log(lat);
            console.log(lng);
        })
    }
}

function collectData() {
    var term = document.getElementById('searchTerm').value;
    var location = document.getElementById('location').value;
    var radius = document.getElementById('rad').value;
    var maxNum = document.getElementById('maxNum').value;
    var deal;
    if (document.getElementById('radio1').value)
        deal = true;
    if (document.getElementById('radio2').value)
        deal = true;
    if (document.getElementById('radio1').value)
        deal = false;

    $.ajax({
        type: "POST",
        url: "/application.html",
        data: {
            'term': term,
            'location': location,
            'radius_filter': radius,
            'limit': maxNum,
            'deals_filter': deal
        },
    })
    return null;
}