// Crear un nuevo objeto Date
var fechaActual = new Date();
// Obtener el día de la semana (0 para domingo, 1 para lunes, etc.)
var diaDeLaSemana = fechaActual.getDay();

// Obtener la hora y los minutos
var horas = fechaActual.getHours();
var minutos = fechaActual.getMinutes();
// Formatear la hora y los minutos como cadena
var horaActual = (horas < 10 ? '0' : '') + horas + ':' + (minutos < 10 ? '0' : '') + minutos;

var year = fechaActual.getFullYear();
var day = fechaActual.getDate();
var month = fechaActual.getMonth() + 1; // Ten en cuenta que los meses van de 0 a 11 en JavaScript
// Formatear la fecha como cadena con ceros a la izquierda si es necesario
var fechaFormateada = year + '-' + (month < 10 ? '0' : '') + month + '-' + (day < 10 ? '0' : '') + day;
// --------------------------------------Ingreso--------------------------------
function insertaIngreso(){
    var respuestaJSON = {"fecha":fechaFormateada, "horaIngreso":horaActual, "diaSemana":diaDeLaSemana};
    $.post('http://localhost:8000/insertarIngreso', respuestaJSON, function(data){
        try{
            console.log(data);
        }
        catch(error){
            console.log(error.message);
        }
    }, "json");
}

function insertaEgreso(){
    var respuestaJSON = {"fecha":fechaFormateada, "horaEgreso":horaActual, "diaSemana":diaDeLaSemana};
    $.post('http://localhost:8000/insertarEgreso', respuestaJSON, function(data){
        try{
            console.log(data);
        }
        catch(error){
            console.log(error.message);
        }
    }, "json");
}


// ---------------------------Funcion mejorada--------------------
// var diasSemana = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado"];

// for (var i = 0; i < diasSemana.length; i++) {
//     var dia = diasSemana[i];
//     generarHorarios(dia);
// }

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
}



function responderPregunta(){ //ObtenerHorario
    var entradas = [];
    var salidas = [];
    var entradaLun = "";
    var salidaLun;
    var fechaActual = new Date();

    // Obtener los componentes de la fecha
    var año = fechaActual.getFullYear();
    var mes = ('0' + (fechaActual.getMonth() + 1)).slice(-2); // Sumar 1 porque los meses son indexados desde 0
    var dia = ('0' + fechaActual.getDate()).slice(-2);

    // Formatear la fecha en el formato "YYYY-mm-dd"
    var fechaFormateada = año + '-' + mes + '-' + dia;
    
    var codigoUsuario = 216666666;
    // for(var i=0; i<diasSemana.length; i++){
    //     entradas[i] = document.getElementById(diasSemana[i]+"Entrada").value;
    //     salidas[i] = document.getElementById(diasSemana[i]+"Salida").value;
    // } 
    // for(var i = 0; i < diasSemana.length; i++){
    //     if(entradas[i] != "N/A"){
            // var respuestaJSON = {"fecha": fechaFormateada, "entrada": entradas[i], "salida": salidas[i], "codigoUsuario": codigoUsuario, "diaSemana": i+1};
            // //console.log(respuestaJSON);
            // $.post('http://localhost:8000/enviar_usuario_horario', respuestaJSON, function(data){
            //     if(data.success == true){
            //         console.log("respuesta del servidor: ", data.message);
            //     }
            // }, "json");           
    //     }
    // }
    entradaLun = document.getElementById("lunesEntrada").value;
    salidaLun = document.getElementById("lunesSalida").value;
    console.log("Entrada lun: ", entradaLun);
    console.log("salida lun: ", salidaLun);
    var respuestaJSON = {"fecha": fechaFormateada, "entrada": entradaLun, "salida": salidaLun, "codigoUsuario": codigoUsuario, "diaSemana": 2};
    //console.log(respuestaJSON);
    $.post("http://localhost:8000/enviar_usuario_horario", respuestaJSON, function(data){
        try{
            console.log('lo que sea');
        }
        catch(error){
            alert(error.message);
        }    
    });           

    // var respuestaJSON = {"dato_que_mandaremos": lunesEntrada, }
    // console.log(queHay);

}

function registroUsuario(){
    
    var codigo = document.getElementById("usuario_cod").value;
    var passw = document.getElementById("pass_usuario").value;
    var nom_usuario = document.getElementById("usuario_nom").value;
    var pass_confirmar = document.getElementById("pass_conf").value;

    if (passw != pass_confirmar){
        console.log("tas wey");
    }
    else{
        console.log("pasas");
        // console.log(codigo);
        // console.log(nom_usuario);
        // console.log(passw);
        var respuestaJSON = {"codigoUsuario":codigo, "nombreUsuario":nom_usuario, "contrasenia":passw};
        console.log(respuestaJSON);
        $.post('http://localhost:8000/insertarUsuario_bd', respuestaJSON, function(data){
            console.log('Jalo el server', data);
            try{
                console.log('lo que sea');
            }
            catch(error){
                console.log(error.message);
            }
        }, "json");
        
    }
}

