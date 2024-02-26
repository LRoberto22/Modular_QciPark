// Custom JavaScript for your website
const {Client} = require('pg')
const client = new Client({
    user: 'avnadmin',
    host: 'modular-parking-modularparking.a.aivencloud.com',
    database: 'defaultdb',
    password: 'AVNS_bJSJ3oB9EynJCouQhPY',
    port: 28916,

})
client.connect(function(err){
    if(err) throw err;
    console.log("Connected");
})
// Function to get the current year and display it
function getYear() {
    var currentDate = new Date();
    var currentYear = currentDate.getFullYear();
    document.querySelector('#displayYear').innerHTML = currentYear;
}

// Call the getYear function to display the current year
getYear();

// Owl Carousel initialization
$('.owl-carousel').owlCarousel({
    loop: true,
    margin: 20,
    nav: true,
    navText: [],
    autoplay: true,
    autoplayHoverPause: true,
    responsive: {
        0: {
            items: 1,
        },
        1000: {
            items: 2,
        },
    },
});

// Google Map initialization
function myMap() {
    var mapProp = {
        center: new google.maps.LatLng(41.25225743727103, 1.0874838588981983),
        zoom: 18,
    };

    var map = new google.maps.Map(
        document.getElementById('googleMap'),
        mapProp
    );

    var marker = new google.maps.Marker({
        position: mapProp.center,
        map: map,
        title: 'Albioljepeto',
    });
}

// Load Google Maps API script
function loadGoogleMapsScript() {
    var script = document.createElement('script');
    script.src =
        'https://maps.googleapis.com/maps/api/js?key=AIzaSyDOR1WpWV_4qqrivGp3XbeYwN-HUq4y8jo&callback=myMap';
    script.defer = true;
    script.async = true;
    document.head.appendChild(script);
}

// Call the function to load the Google Maps API script
loadGoogleMapsScript();
