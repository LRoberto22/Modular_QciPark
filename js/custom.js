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
    var opcionNAE = document.createElement("option");
    // ----------Para la entrada---------------------
    for (var i = 0; i <= 12; i++){
        opciones[i] = document.createElement("option");
        opciones[i].text = (i+7)+":00";
        opciones[i].value = (i+7)+":00";
        selectEntrada.append(opciones[i]);
    }
    opcionNAE.text = "N/A";
    opcionNAE.value = "N/A";
    selectEntrada.append(opcionNAE);
    // ----------Para la salida---------------------
    for (var i = 0; i <= 13; i++){
        opciones[i] = document.createElement("option");
        opciones[i].text = (i+8)+":00";
        opciones[i].value = (i+8)+":00";
        selectSalida.append(opciones[i]);
    }
    opcionNA.text = "N/A";
    opcionNA.value = "N/A";
    selectSalida.append(opcionNA);
}



function responderPregunta(){
    var horarios = [[],[]];
    diasSemana.forEach(function(dia, indice) {
        alert(dia);
        horarios[indice][0] = document.getElementById(dia+"Entrada").value;
        alert(horarios[indice][0]);
        horarios[indice][1] = document.getElementById(dia+"Salida").value;
        alert(horarios[indice][1]);
    });
    
    
   
    // var respuestaJSON = {"dato_que_mandaremos": lunesEntrada, }
    // console.log(queHay);

}