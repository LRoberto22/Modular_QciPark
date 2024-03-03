

// Function to get the current year and display it
function getYear() {
    var currentDate = new Date();
    var currentYear = currentDate.getFullYear();
    document.querySelector('#displayYear').innerHTML = currentYear;
}

