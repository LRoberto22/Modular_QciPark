// var selectExistente = document.getElementById("lunesEntrada");
// var opciones = [];
// for( var i = 0; i <= 14; i++){
//     opciones[i] = document.createElement("option");
//     opciones[i].text = (i+7)+":00";
//     opciones[i].value = (i+7)+":00";
//     selectExistente.append(opciones[i]);
// }
// var opcionNA = document.createElement("option");
// opcionNA.text = "N/A";
// opcionNA.value = "N/A";
// selectExistente.append(opcionNA);

// ---------------------------Funcion mejorada--------------------
var diasSemana = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado"];

for (var i = 0; i < diasSemana.length; i++) {
    var dia = diasSemana[i];
    generarHorarios(dia);
}

function generarHorarios(dia){
    var opciones = [];
    var selectEntrada = document.getElementById(dia+"Entrada");
    var selectSalida = document.getElementById(dia+"Salida");
    var opcionNA = document.createElement("option");
    // ----------Para la entrada---------------------
    for (var i = 0; i <= 14; i++){
        opciones[i] = document.createElement("option");
        opciones[i].text = (i+7)+":00";
        opciones[i].value = (i+7)+":00";
        selectEntrada.append(opciones[i]);
    }
    opcionNA.text = "N/A";
    opcionNA.value = "N/A";
    selectEntrada.append(opcionNA);
    // ----------Para la salida---------------------
    for (var i = 0; i <= 14; i++){
        opciones[i] = document.createElement("option");
        opciones[i].text = (i+7)+":00";
        opciones[i].value = (i+7)+":00";
        selectSalida.append(opciones[i]);
    }
    opcionNA.text = "N/A";
    opcionNA.value = "N/A";
    selectSalida.append(opcionNA);
}