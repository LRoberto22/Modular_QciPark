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
var cuposTotales = 500;

var year = fechaActual.getFullYear();
var day = fechaActual.getDate();
var month = fechaActual.getMonth() + 1; // Los meses van de 0 a 11 por eso el + 1
// Formatear la fecha como cadena con ceros a la izquierda si es necesario
var fechaFormateada = year + '-' + (month < 10 ? '0' : '') + month + '-' + (day < 10 ? '0' : '') + day;


//-----------------------------------------CONSULTAR CUPO ACTUAL------------------------------------------
function consultaCupo(){
    document.getElementById("horaActualizacion").textContent = horaActual;
    var respuestaJSON = {"fecha":fechaFormateada, "diaSemana":diaDeLaSemana};
    $.post('http://localhost:8000/consultaCupo', respuestaJSON, function(data){
        try{
            console.log(data);
            let cuposDisponibles = parseInt(data);
            document.getElementById("cuposDisponibles").textContent = "Cupos disponibles: "+ (cuposTotales + cuposDisponibles)
            updateProgressBar(((cuposTotales + cuposDisponibles)/500)*100);
        }
        catch(error){
            console.log(error);
        }
    }, "json");
}

function updateProgressBar(percentage) {
    // Ajusta la anchura de las barras de progreso
    const progressBar = document.querySelector('.progress-bar');
    progressBar.style.width = percentage + '%';
    
    // Muestra el porcentaje dentro de la barra de progreso
    progressBar.textContent = percentage.toFixed(1) + '%';
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
    var respuestaJSON = {"diaSemanaActual":diaDeLaSemana, "usuario": codigoLogin}; //Lo enviamos al endpoint
    console.log(respuestaJSON);
    //document.getElementById("nombreUser").textContent = nombreLogin;
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

function getHoraPico() {
    var respuestaJSON = { "dia": diaDeLaSemana }; //Lo enviamos al endpoint
    console.log(respuestaJSON);
    $.get('http://localhost:8000/horas_actividad/', respuestaJSON, function (data) { //Data nos retorna la consulta a la bd
        try {
            console.log(data);
            $('#horaPicoIngresos').text('HORA PICO: ' + convertirFormato12Horas(data.hora_pico_ingresos));
            $('#horaMenosActividadIngresos').text('HORA MÁS TRANQUILA: ' + convertirFormato12Horas(data.hora_menos_actividad_ingresos));
            $('#horaPicoEgresos').text('HORA PICO: ' + convertirFormato12Horas(data.hora_pico_egresos));
            $('#horaMenosActividadEgresos').text('HORA MÁS TRANQUILA: ' + convertirFormato12Horas(data.hora_menos_actividad_egresos));
        } catch (error) {
            console.log(error);
        }
    }, "json");
}

// Función para convertir formato de 24 horas a 12 horas
function convertirFormato12Horas(hora24) {
    var partesHora = hora24.split(':');
    var horas = parseInt(partesHora[0]);
    var minutos = parseInt(partesHora[1]);
    var periodo = (horas >= 12) ? 'PM' : 'AM';
    horas = (horas > 12) ? horas - 12 : horas;
    horas = (horas == 0) ? 12 : horas;
    horas = (horas < 10) ? '0' + horas : horas;
    minutos = (minutos < 10) ? '0' + minutos : minutos;
    return horas + ':' + minutos + ' ' + periodo;
}


//-------------------------------------OBTENER EL HORARIO DEL USUARIO----------------------------------
function getHorario(){
    var diasClase = [];
    var respuestaJSON = {"usr": codigoLogin};
    $.post('http://localhost:8000/consultaHorario', respuestaJSON, function(data){
        try{
            if(data!=0){
                document.getElementById("nombreUser").textContent = nombreLogin;
                console.log(data);
                arraysData = data[0];
                console.log("arrays data: ",arraysData[0].length);
                for(var i = 0; i<arraysData.length; i++){
                    diasClase[i] = arraysData[i][2];
                }
                console.log(diasSemana[0]);
                console.log(diasSemana[1]);
                console.log(diasSemana[2]);
                console.log(diasSemana[3]);
                console.log(diasSemana[4]);
                console.log(diasSemana[5]);
                for(var j = 0; j<diasClase.length; j++){
                    var diaEntrada = document.getElementById(diasSemana[arraysData[j][2]]+"Entra");
                    var diaSalida = document.getElementById(diasSemana[arraysData[j][2]]+"Salida");
                    entradaFormateada = arraysData[j][0];
                    salidaFormateada = arraysData[j][1];
                    entradaFormateada = entradaFormateada.split(":");
                    salidaFormateada = salidaFormateada.split(":");
                    diaEntrada.textContent = entradaFormateada[0]+":"+entradaFormateada[1]; //Hora de entrada
                    diaSalida.textContent = salidaFormateada[0]+":"+salidaFormateada[1]; //Hora de salida


                    $.get('http://localhost:8000/hora_menos_actividad_antes/?dia=' + i + '&hora=' + entradaFormateada.join(":"),
                        function(response) {
                            console.log(response);
                            var labelId = diasSemana[response.dia] + "Extra";
                            // Obtener la hora y los minutos de la cadena de tiempo
                            var horaSinSegundos = response.hora_menos_actividad_antes.split(":").slice(0, 2).join(":");
                            // Actualizar el contenido del label con la hora y los minutos
                            $("#" + labelId).text(horaSinSegundos);
                            // Aquí puedes actualizar tu label con la mejor hora obtenida
                            // response.hora_menos_actividad_antes contiene la mejor hora
                        }); 
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
    var codigoUsuario = codigoLogin;
    //window.location.href="usuario.html";
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
                        window.location.href="usuario.html";
                    }
                    catch(error){
                        console.log(error);
                    }
                },"json");           
        }
    }
}

//--------------------------------------Obtener Horario del ususario-----------------------------
function existeHorario(){
    var respuestaJSON = {"usr": codigoLogin};
    $.post('http://localhost:8000/consultaHorario', respuestaJSON, function(data){
        try{
            if(data == 0){
                document.getElementById("tituloHorario").textContent = "Al parecer no tienes horario registrado ingresa el tuyo!";
            }
            else{
                console.log("si tiene ", data);
                //window.location.href = "usuario.html";
            }       
        }
        catch(error){
            console.log(error);
        }
    }, "json");
}

//--------------------------------------Obtener Horario del ususario para la ventana usuario-----------------------------

function existeHorarioUsuario(){
    var respuestaJSON = {"usr": codigoLogin};
    $.post('http://localhost:8000/consultaHorario', respuestaJSON, function(data){
        if(data == 0){
            alert("No tienes horario Jalate a registrarlo");
            location.href = "ingreso_horarios.html";
        }
        else{
            console.log("si tiene ", data);
        }
    }, "json");
}
//------------------------------------- REGISTRAR USUARIO -------------------------------------

function registroUsuario(){
    var codigo = document.getElementById("usuario_cod").value;
    var passw = document.getElementById("pass_usuario").value;
    var nom_usuario = document.getElementById("usuario_nom").value;
    var pass_confirmar = document.getElementById("pass_conf").value;

    if (passw != pass_confirmar){
        alert("Contraseñas no coinciden");
        document.getElementById("pass_usuario").value="";
        document.getElementById("pass_conf").value="";
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
                        localStorage.setItem('codigoUsuario', codigo);
                        localStorage.setItem('nombreUsuario', nom_usuario);
                        
                        window.location.href = "index.html";
                        
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

            localStorage.setItem('codigoUsuario', data.logeado[0]);
            localStorage.setItem('nombreUsuario', data.logeado[1]);

            // codigoLogin = localStorage.getItem('codigoUsuario');
            // nombreLogin = localStorage.getItem('nombreUsuario' );

            location.href = "index.html";
    
        }   
        else{
            console.log("Datos incorrectos");
            alert("Datos incorrectos... Vuelve a intentarlo");
            document.getElementById("codigoUsu").value = "";
            document.getElementById("passUsu").value = "";

        }
    });

}


//------------------------------------- CERRAR SESION -------------------------------------
function cerrarSesion(){
    codigoLogin = null;
    nombreLogin = null;

    localStorage.removeItem('codigoUsuario');
    localStorage.removeItem('nombreUsuario');

    window.location.href = 'inicioSesion.html';
}

//------------------------------------- VERIFICAR QUE HAYA SESION -------------------------------------
function checarSesion(){
    if (codigoLogin === null || nombreLogin === null) {
        // Redirige a otra página
        window.location.href = 'inicioSesion.html';
    }
}

function existeSesion(){
    if (codigoLogin != null){
        window.location.href = 'index.html';
    }
}

//------------------------------------- CANCELAR REGISTRO -------------------------------------
function cancelarRegistro(){
    location.href = "inicioSesion.html";
}


// Hacer la solicitud al endpoint para obtener los datos
function grafica() {
    // Realizar la solicitud GET para obtener los datos
    $.get('http://localhost:8000/actividad_promedio_semanal/')
    .done(function(data) {
        // Verificar si se recibieron datos válidos
        if (data && Object.keys(data).length > 0) {
            // Cambiar los nombres de las columnas
            const etiquetas = {
                "0": "Lunes",
                "1": "Martes",
                "2": "Miércoles",
                "3": "Jueves",
                "4": "Viernes",
                "5": "Sábado"
            };

            // Obtener los valores y las etiquetas
            const valores = Object.values(data);
            const labels = Object.keys(etiquetas).map(key => etiquetas[key]);

            // Crear el gráfico
            const ctx = document.getElementById('miGrafica').getContext('2d');
            const miGrafica = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'ACTIVIDAD',
                        data: valores,
                        backgroundColor: 'rgba(255, 165, 0, 0.2)', // Naranja transparente
                        borderColor: 'rgba(255, 165, 0, 1)', // Naranja sólido
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        xAxes: [{
                            ticks: {
                                beginAtZero: true
                            },
                            gridLines: {
                                color: 'rgba(255, 255, 255, 0.1)' // Color blanco para las líneas de la cuadrícula del eje X
                            }
                        }],
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            },
                            gridLines: {
                                color: 'rgba(255, 255, 255, 0.1)' // Color blanco para las líneas de la cuadrícula del eje Y
                            }
                        }]
                    },
                    legend: {
                        labels: {
                            fontColor: 'white' // Color blanco para las etiquetas de la leyenda
                        }
                    },
                    rotation: -90,
                    plugins: {
                        datalabels: {
                            color: 'white' // Color blanco para las etiquetas de datos
                        }
                    }
                }
            });
        } else {
            console.error('No se recibieron datos válidos.');
        }
    })
    .fail(function(error) {
        console.error('Error al obtener los datos:', error);
    });
}
