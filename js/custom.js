//------------------------------------- VARIBABLES GLOBALES -------------------------------------
// Variables para la verificacion del Login
var codigoLogin, nombreLogin;

codigoLogin = localStorage.getItem('codigoUsuario');
nombreLogin = localStorage.getItem('nombreUsuario' );

console.log("Datos guardados en localStorage:");
console.log("Código de usuario:", codigoLogin);
console.log("Nombre de usuario:", nombreLogin);

var diasSemana = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado"];
// Crear un nuevo objeto Date
var fechaActual = new Date();
// Obtener el día de la semana (0 para lunes, 1 para martes etc.)
var diaDeLaSemana = (fechaActual.getDay() -1 + 7) % 7;

// Obtener la hora y los minutos
var horas = fechaActual.getHours();
var minutos = fechaActual.getMinutes();
// Formatear la hora y los minutos como cadena
var horaActual = (horas < 10 ? '0' : '') + horas + ':' + (minutos < 10 ? '0' : '') + minutos;

//Es para cuando tengamos las variables de sesion, solamente sustituyamos
var usuarioAUX = 216666666;
//Cupos totales seteados ya que no tneemos la información oficial 
var cuposTotales = 999;

var year = fechaActual.getFullYear();
var day = fechaActual.getDate();
var month = fechaActual.getMonth() + 1; // Los meses van de 0 a 11 por eso el + 1
// Formatear la fecha como cadena con ceros a la izquierda si es necesario
var fechaFormateada = year + '-' + (month < 10 ? '0' : '') + month + '-' + (day < 10 ? '0' : '') + day;

//-----------------------------------------CONSULTAAR CUPO ACTUAL------------------------------------------
function consultaCupo(){
    document.getElementById("horaActualizacion").textContent = horaActual;
    var respuestaJSON = {"fecha":fechaFormateada, "diaSemana":diaDeLaSemana};
    $.post('http://localhost:8000/consultaCupo', respuestaJSON, function(data){
        try{
            console.log(data);
            let cuposDisponibles = parseInt(data);
            document.getElementById("cuposDisponibles").textContent = cuposTotales + cuposDisponibles
        }
        catch(error){
            console.log(error.message);
        }
    }, "json");
}

// -------------------------------------- BOTON INGRESO --------------------------------
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
    location.reload();
}

//------------------------------------- BOTON DE EGRESO -------------------------------------

function insertaEgreso(){
    var respuestaJSON = {"fecha":fechaFormateada, "horaEgreso":horaActual, "diaSemana":diaDeLaSemana};
    $.post('http://localhost:8000/insertarEgreso', respuestaJSON, function(data){
        try{
            console.log(data);
        }
        catch(error){
            console.log(error);
        }
    }, "json");
    location.reload();
}

// -------------------------------- VALIDACION DEL LAS HORAS EN EL HORARIO --------------------------

function cambioHorario(selectElement) {
    var opciones = [];
    //Obtener la seleccion actual de entrada
    var seleccion = selectElement.value;
    //obtener el dia de entrada
    var diaId = selectElement.id;
    var dia = diaId.replace("Entrada", "");
    //Obtener la hora de entrada
    var entrada = parseInt(seleccion.replace(":00", ""));
    //Select de salida
    var select2 = document.getElementById(dia+"Salida");
        
    if (seleccion === "N/A") {
        select2.disabled = true;
    } else {
        select2.disabled = false;
        select2.options.length = 0;
        for (var i = 1; i <= (21-entrada); i++){
            opciones[i] = document.createElement("option");
            opciones[i].text = (entrada + i)+":00";
            opciones[i].value = (entrada+ i)+":00";
            select2.append(opciones[i]);
        }
    }
  }

//--------------------------------------OBTENER LA ENTRADA Y SALIDA DEL USUARIO-----------------------------------------------
function getEntradaSalida(){
    var respuestaJSON = {"diaSemanaActual":diaDeLaSemana, "usuario": usuarioAUX}; //Lo enviamos al endpoint
    console.log(respuestaJSON);
    document.getElementById("diaHoy").textContent = diasSemana[diaDeLaSemana];   //Dia actual
    $.post('http://localhost:8000/getEntradaSalida', respuestaJSON, function(data){ //Data nos retorna la consulta a la bd
        try{   
            entradaFormateada = data[0][0];
            entradaFormateada = entradaFormateada.split(":");
            salidaFormateada = data[0][1];
            salidaFormateada = salidaFormateada.split(":");
            document.getElementById("entradaHoy").textContent = entradaFormateada[0]+":"+entradaFormateada[1] //Hora de entrada
            document.getElementById("salidaHoy").textContent = salidaFormateada[0]+":"+salidaFormateada[1];  //Hora de salida 
        }
        catch(error){
            console.log(error);
        }
    }, "json");
}

//-------------------------------------OBTENER EL HORARIO DEL USUARIO----------------------------------
function getHorario(){
    var diasClase = [];
    var respuestaJSON = {"usr": usuarioAUX};
    $.post('http://localhost:8000/consultaHorario', respuestaJSON, function(data){
        try{
            console.log(data);
            arraysData = data[0];
            console.log("arrays data: ",arraysData[0].length);
            var diasClase = [];
            for(var i = 0; i<arraysData.length; i++){
                diasClase[i] = arraysData[i][2];
                
                for(var j = 0; j < (arraysData[i].length) - 1; j++){
                    console.log("horarios: ", arraysData[i][j]);
                    
                }
            }
            for(var i=0; i<diasSemana.length; i++){
                var diaEntrada = document.getElementById(diasSemana[i]+"Entra");
                var diaSalida = document.getElementById(diasSemana[i]+"Salida");
                if(diasClase.includes(i)){
                    diaEntrada.textContent = "{";
                    diaSalida.textContent = "]";
                } else{
                    diaEntrada.textContent = "No hay";
                    diaSalida.textContent = "no hay";
                }

            }
            
        }
        catch(error){
            console.log(error);
        }
    }, "json");
}

//--------------------------------------GENERAR HORAS DE ENTRADA Y SALIDA--------------------------------
function generarHorarios(dia){
    var opciones = [];

    var selectEntrada = document.getElementById(dia+"Entrada");
    var selectSalida = document.getElementById(dia+"Salida");
    var opcionNAE = document.createElement("option");
    // ----------Para la entrada---------------------
    for (var i = 0; i <= 13; i++){
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
}


//------------------------------------- GUARDAR HORARIO DE USUARIO -------------------------------------
function guardarHorario(){
    var entradas = [];
    var salidas = [];
    var codigoUsuario = usuarioAUX;
    for(var i=0; i<diasSemana.length; i++){
        entradas[i] = document.getElementById(diasSemana[i]+"Entrada").value;
        salidas[i] = document.getElementById(diasSemana[i]+"Salida").value;
    } 
    for(var i = 0; i < diasSemana.length; i++){
        if(entradas[i] != "N/A"){
            var respuestaJSON = {"entrada": entradas[i], "salida": salidas[i], "codigoUsuario": codigoUsuario, "diaSemana": i};
            console.log(respuestaJSON);
            console.log("DIAS: ",i);
                $.post('http://localhost:8000/enviarUsuarioHorario', respuestaJSON, function(data){
                    try{
                        console.log(data);
                    }
                    catch(error){
                        console.log(error);
                    }
                }, "json");           
        }
    }
}

//------------------------------------- REGISTRAR USUARIO -------------------------------------

function registroUsuario(){
    var codigo = document.getElementById("usuario_cod").value;
    var passw = document.getElementById("pass_usuario").value;
    var nom_usuario = document.getElementById("usuario_nom").value;
    var pass_confirmar = document.getElementById("pass_conf").value;

    if (passw != pass_confirmar){
        console.log("tas wey");
    }
    else{
        $.post('http://localhost:8000/verificarUsuario', {codigoUsuario: codigo}, function(data){
            console.log(data);
            if(data.existe){
                alert("El codigo ya tiene un usuario registrado");
            }
            else{
                var respuestaJSON = {"codigoUsuario":codigo, "nombreUsuario":nom_usuario, "contrasenia":passw};
                console.log(respuestaJSON);
                $.post('http://localhost:8000/insertarUsuario_bd', respuestaJSON, function(data){
                    console.log('Jalo el server', data);
                    try{
                        console.log(data);
                        //location.href = "inicioSesion.html"
                    }
                    catch(error){
                        console.log(error);
                    }
                }, "json");
            }
        }, "json");
    }
}

//------------------------------------- VERIFICAR LOGIN -------------------------------------



function verificarLogin(){
    var codigo = document.getElementById("codigoUsu").value;
    var pass = document.getElementById("passUsu").value;

    var respuestaJSON = {"codigoUsuario":codigo, "contrasenia":pass};


    $.post('http://localhost:8000/verificacionLogin', respuestaJSON, function(data){
        console.log(data);
        if (data.existe){
            console.log("Que chingon");

            localStorage.setItem('codigoUsuario', data.logeado[0]);
            localStorage.setItem('nombreUsuario', data.logeado[1]);

            // codigoLogin = localStorage.getItem('codigoUsuario');
            // nombreLogin = localStorage.getItem('nombreUsuario' );

            location.href = "index.html";
    
        }   
        else{
            console.log("Datos incorrectos");
            // codigo.value = '';
            // pass.value = '';
        }
    });

}


//------------------------------------- CERRAR SESION -------------------------------------
function cerrarSesion(){
    codigoLogin = null;
    nombreLogin = null;

    localStorage.removeItem('codigoUsuario');
    localStorage.removeItem('nombreUsuario');
}

//------------------------------------- VERIFICAR QUE HAYA SESION -------------------------------------
// function checarSesion(){
//     if (codigoLogin === null || nombreLogin === null) {
//         // Redirige a otra página
//         window.location.href = 'inicioSesion.html';
//     }
// }

