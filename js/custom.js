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
}



function responderPregunta(){ //ObtenerHorario
    var entradas = [];
    var salidas = [];
    var diasAsiste = [];
    var fechaActual = new Date();

    // Obtener los componentes de la fecha
    var año = fechaActual.getFullYear();
    var mes = ('0' + (fechaActual.getMonth() + 1)).slice(-2); // Sumar 1 porque los meses son indexados desde 0
    var dia = ('0' + fechaActual.getDate()).slice(-2);

    // Formatear la fecha en el formato "YYYY-mm-dd"
    var fechaFormateada = año + '-' + mes + '-' + dia;
    
    var codigoUsuario = 216666666;
    for(var i=0; i<diasSemana.length; i++){
        entradas[i] = document.getElementById(diasSemana[i]+"Entrada").value;
        salidas[i] = document.getElementById(diasSemana[i]+"Salida").value;
    } 
    for(var i = 0; i < diasSemana.length; i++){
        if(entradas[i] != "N/A"){
            console.log("se hace insercion en BD");
            // var respuestaJSON = {"fecha": fechaFormateada, "entrada": entradas[i], "salida": salidas[i], "codigoUsuario": codigoUsuario, "diaSemana": i};
            // $.post('http://0.0.0.0:8000/obtener-usuario-horario', respuestaJSON, function(data){
            //     console.log("respuesta del servidor: ", data.message);
            // });

            $.ajax({
                url: 'http://0.0.0.0:8000/obtener-usuario-horario',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(respuestaJSON),
                success: function(data) {
                    console.log("respuesta del servidor:", data.message);
                }
            });
        }
    }

    // var respuestaJSON = {"dato_que_mandaremos": lunesEntrada, }
    // console.log(queHay);

}

function registroUsuario(){
    
    var codigo = document.getElementById("usuario_cod").value;
    var nom_usuario = document.getElementById("usuario_nom").value;
    var pass = document.getElementById("usuario_pass").value;
    var pass_confirmar = document.getElementById("pass_conf").value;

    console.log(codigo);
    console.log(nom_usuario);
    console.log(pass);

    if (pass =! pass_confirmar){
        console.log("tas wey");
    }
    else{
        console.log("pasas");
        console.log("pasas");
        var respuestaJSON = {"codigoUsuario":codigo, "nombreUsuario":nom_usuario, "contrasenia":pass}
        $.post('https://0.0.0.0:8000/insertarUsuario_bd', respuestaJSON, function(data){
            console.log('Jalo el server', data);
        });
        
    }
}