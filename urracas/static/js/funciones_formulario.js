// Funciones de inicializacion del formulario principal
function initialize() {
  // Inicializa el mapa
  var myOptions = {
    zoom: 14,
    center: new google.maps.LatLng(42.81211, -1.64922),
    mapTypeControl: true,
    mapTypeControlOptions: {style: google.maps.MapTypeControlStyle.DROPDOWN_MENU},
    navigationControl: true,
    mapTypeId: google.maps.MapTypeId.SATELLITE,
    tilt: 0
  }
  map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
  
  // Crea los polígonos de areas en el mapa
  areaTaconera.setMap(map);
  areaCampus.setMap(map);
  areaCastanos.setMap(map);
  areaCiudadela.setMap(map);
  
  // Añade click handler para guardar coordenadas
  google.maps.event.addListener(map, 'click', exportCoordinates);
  google.maps.event.addListener(areaTaconera, 'click', exportCoordinates);
  google.maps.event.addListener(areaCampus, 'click', exportCoordinates);
  google.maps.event.addListener(areaCastanos, 'click', exportCoordinates);
  google.maps.event.addListener(areaCiudadela, 'click', exportCoordinates);
  
  // Pone valores por defecto en los campos de coordenadas y fecha
  $("#lat").val("");
  $("#lng").val("");
  $("#momento").val("");
  
  // Desactiva el campo de anilla extra
  $("#extraanilla").prop("checked", false);
  mostrarExtraAnilla();
  
  // Muestra los selectores de anillas o el bloque de cuantas urracas
  activarAnillas();
  
  // Inicializa el selector de fecha y hora
  $("#momentopicker").datetimepicker({
    showTodayButton: true,
    defaultDate: new Date(),
    useCurrent: false,
    minDate: new Date('09/01/2014'),
    maxDate: new Date(),
    locale: 'es'
  });
}


// Muestra el campo de anilla extra y el modal con instrucciones, si se marca
function mostrarExtraAnilla() {
    if ($('#extraanilla').prop("checked")) {
        $("#extraAnillaModal").modal('show');
        $('#RMBlock').removeClass('hide');
    } else {
        $('#RMBlock').addClass('hide');
    }
}


// Muestra los selectores de anillas o el bloque de cuantas urracas
function activarAnillas() {
    if ($("#conAnillas").prop("checked")) {
        // Mostrar los bloques de anillas
		$("#Ldiv").show();
        $("#Rdiv").show();
		$("#3div").show();
		$("#RMBlock").show();
		// (des)activar los bloques de anillas
		$("#RT").prop("disabled", false);
		$("#LB").prop("disabled", false);
		$("#LT").prop("disabled", true);
		// Ocultar el bloque de cuantas urracas
		$("#cuantasUrracasDiv").hide();
		// Establecer cuantas urracas en 1
		$("cuantas").val("1");
        // Activar o desactivar anilla izquierda superior
        enableLT();
    } else {
		// Ocultar los bloques de anillas
        $("#RT").val("");
        $("#LB").val("");
        $("#LT").val("");
        $("#RM").val("");
        $("#Ldiv").hide();
        $("#Rdiv").hide();
		$("#3div").hide();
		$("#RMBlock").hide();
		// Mostrar el bloque de cuantas urracas
		$("#cuantasUrracasDiv").show();
    }
}


// Activar o desactivar anilla izquierda superior
function enableLT() {
    if ($("#LB").val() == "") {
        $("#LT").val("");
        $("#LT").prop('disabled', true);
    } else {
        $("#LT").prop('disabled', false);
    }
}


// Muestra el valor del momento en el campo "momento" al pulsar el boton
function activarAhora() {
    var hoy = new Date;
	var dd = hoy.getDate();
    var mm = hoy.getMonth()+1; //January is 0!
    var yyyy = hoy.getFullYear();
    var h = hoy.getHours();
    var m = hoy.getMinutes();
    
    if (dd<10) {
        dd = '0'+dd;
    }
    if (mm<10) {
        mm = '0'+mm;
    }
    if (h<10) {
        h = '0'+h;
    }
    if (m<10) {
        m = '0'+m;
    }
    ahora = yyyy+'/'+mm+'/'+dd+' '+h+':'+m;
    $('#momento').val(ahora);
}


// (Des)activa el campo "actividad" segun el valor de "muerta"
function desactivarActividad() {
    if ($("#muerta").prop("checked")) {
        $("#actividad").prop("disabled", true);
    } else {
		$("#actividad").prop("disabled", false);
    }
}


// Comprobaciones previas al envio de los datos
function compruebaCodigo(codigos) {
    // Comprobaciones de complecion
    if ($('#momento').val() == "") {
        $('#problemaModalLabel').text('CUIDADO: Faltan la fecha y hora');
        $('#descripcionProblema').text('No nos has dicho en qué momento viste a la urraca. Por favor, pulsa en el selector de fecha y hora (el icono del calendario) para indicar la fecha y hora y poder continuar.');
        $('#problemaModal').modal();
        return;
    } else if ($('#lat').val() == "") {
        $('#problemaModalLabel').text('CUIDADO: Falta el punto en el mapa');
        $('#descripcionProblema').text('No nos has dicho dónde has visto a la urraca. Por favor, indica un punto en el mapa para poder continuar.');
        $('#problemaModal').modal();
        return;
    }
    
    // Comprueba que, si la urraca no tiene anillas, cae dentro de algun poligono
    if (!($('#conAnillas').prop('checked'))) {
        // Saca el punto
        var punto = new google.maps.LatLng($('#lat').val(), $('#lng').val());
        var dentro = false;
        
        // Taconera
        if (google.maps.geometry.poly.containsLocation(punto, areaTaconera)) {
            dentro = true;
        // Campus
        } else if (google.maps.geometry.poly.containsLocation(punto, areaCampus)) {
            dentro = true;
        // Castanos
        } else if (google.maps.geometry.poly.containsLocation(punto, areaCastanos)) {
            dentro = true;
        // Ciudadela
        } else if (google.maps.geometry.poly.containsLocation(punto, areaCiudadela)) {
            dentro = true;
        } else {
            dentro = false;
        }
        
        // Si no esta dentro de ningun area, no se envia
        if (!(dentro)) {
            $('#problemaModalLabel').text('CUIDADO: Ave sin anillas fuera de las zonas coloreadas');
            $('#descripcionProblema').text('Como decíamos en las instrucciones, si has visto una urraca sin anilla, sólo puedes informarnos del avistamiento si ésta estaba dentro de alguna de las áreas coloreadas del mapa (parque de la taconera, ciudadela o campus de la Universidad de Navarra). Si la urraca que has visto no tenía anillas y no estaba dentro de una de estas zonas, lamentablemente el dato no resulta de utilidad para el estudio, así que no podemos aceptarlo.');
            $('#problemaModal').modal();
            return;
        // Si esta dentro de un area, se envia sin apadrinar
        } else {
            $("#dataform").submit();
            return;
        }
    }
    
    // Si alguna de las anillas es de color desconocido, no se puede apadrinar
    if ($("#RT").val() == 'desconocido' || $("#LT").val() == 'desconocido' || $("#LB").val() == 'desconocido' || $("#RM").val() == 'desconocido') {
        $("#dataform").submit();
        return;
    }
    
    // Se genera el codigo de colores
    var codigo = $("#RT").val().concat("-", $("#LB").val(), "-", $("#LT").val());
    // Se comprueba que el codigo existe en la lista
    // Si existe, se envia
    if ($.inArray(codigo, codigos)>-1) {
        $("#dataform").submit();
    // Si no existe, se pide confirmacion
    } else {
        $("#confirmacionCodigo").modal('show');
    }

}


// DEPRECADAS //
/*

function noApadrinar() {
    $("#apadrinar").val(false);
    $("#apadrinamientoForm").submit();
}

function apadrinar() {
    $("#apadrinar").val(true);
    $("#apadrinamientoForm").submit();
}


*/