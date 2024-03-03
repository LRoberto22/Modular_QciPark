$(document).ready(function() {

    // Function to get the current year and display it
    function getYear() {
        var currentDate = new Date();
        var currentYear = currentDate.getFullYear();
        document.querySelector('#displayYear').innerHTML = currentYear;
    }

    function obtenerPregunta() {
        $.get('http://0.0.0.0:8000/obtener-usuario-horario', function(data) {
            console.log("Desayuna con huevo");
            if (data) {
                salida = data.salida;
                console.log(salida);
                $('.Salida').text("Quisiera ser una mosca");
            } else {
                console.log("No jalo");  
            }
        });
    }
});