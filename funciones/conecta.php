<?php

//Le ando calando para ver como conectar esta madre

define("HOST",'localhost');
define("BD",'empresa');
define("USER_BD",'root');
define("PASS_BD",'');

function conecta(){
    $con = new mysqli(HOST, USER_BD, PASS_BD, BD);
    return $con;
}

?>