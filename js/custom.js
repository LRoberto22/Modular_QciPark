//------------------------------------- VARIBABLES GLOBALES -------------------------------------
// Variables para la verificacion del Login
var codigoLogin, nombreLogin;

codigoLogin = localStorage.getItem('codigoUsuario');
nombreLogin = localStorage.getItem('nombreUsuario' );

console.log("Datos guardados en localStorage:");
console.log("Código de usuario:", codigoLogin);
console.log("Nombre de usuario:", nombreLogin);

// Crear un nuevo objeto Date
var fechaActual = new Date();
// Obtener el día de la semana (0 para domingo, 1 para lunes, etc.)
var diaDeLaSemana = fechaActual.getDay();

// Obtener la hora y los minutos
var horas = fechaActual.getHours();
var minutos = fechaActual.getMinutes();
// Formatear la hora y los minutos como cadena
var horaActual = (horas < 10 ? '0' : '') + horas + ':' + (minutos < 10 ? '0' : '') + minutos;

//Es para cuando tengamos las variables de sesion, solamente sustituyamos
var usuarioAUX = 216666666;

var year = fechaActual.getFullYear();
var day = fechaActual.getDate();
var month = fechaActual.getMonth() + 1; // Ten en cuenta que los meses van de 0 a 11 en JavaScript
// Formatear la fecha como cadena con ceros a la izquierda si es necesario
var fechaFormateada = year + '-' + (month < 10 ? '0' : '') + month + '-' + (day < 10 ? '0' : '') + day;

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
            console.log(error.message);
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
    // for (var i = 0; i < diasSemana.length; i++){
    var select2 = document.getElementById(dia+"Salida");
        //     // Habilitar o deshabilitar el segundo select basado en la selección del primero
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

//------------------------------------- GUARDAR HORARIO DE USUARIO -------------------------------------
function guardarHorario(){
    var diasSemana = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado"];
    var entradas = [];
    var salidas = [];
    var entradaLun = "";
    var salidaLun;

    var codigoUsuario = usuarioAUX;
    for(var i=0; i<diasSemana.length; i++){
        entradas[i] = document.getElementById(diasSemana[i]+"Entrada").value;
        salidas[i] = document.getElementById(diasSemana[i]+"Salida").value;
    } 
    for(var i = 0; i < diasSemana.length; i++){
        if(entradas[i] != "N/A"){
            var respuestaJSON = {"entrada": entradas[i], "salida": salidas[i], "codigoUsuario": codigoUsuario, "diaSemana": i+1};
            console.log(respuestaJSON);
            $.post('http://localhost:8000/enviarUsuarioHorario', respuestaJSON, function(data){
                try{
                    console.log(data);
                }
                catch(error){
                    console.log(error.message);
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
                        console.log(error.message);
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
function checarSesion(){
    if (codigoLogin === null || nombreLogin === null) {
        // Redirige a otra página
        window.location.href = 'inicioSesion.html';
    }
}

