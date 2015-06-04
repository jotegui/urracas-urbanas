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
}

activarHoy = function() {
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth()+1; //January is 0!
    var yyyy = today.getFullYear();

    if(dd<10) {
        dd='0'+dd;
    } 

    if(mm<10) {
        mm='0'+mm;
    } 

    today = yyyy+'-'+mm+'-'+dd;
    $('#FECHA').val(today);
}

$(function() {
  $('.datepicker').datepicker({
    format: 'yyyy-mm-dd',
	startDate: new Date('09/01/2014'),
	endDate: new Date(),
	language: 'es-ES',
    todayBtn: 'linked',
    todayHighlight: true,
    autoclose: true
  });
  
  $('.timepicker').datetimepicker({
      format: 'LT',
      locale: 'es'
    });
});

enableID = function(targetID) {
    $('#'+targetID).prop("disabled", false);
}

disableID = function(targetID) {
    $('#'+targetID).prop("disabled", true);
}


// Comprueba que los datos basicos han sido rellenados y envia el formulario
function compruebaAnillamiento() {
    if ($("#lat").val() == "") {
        $('#problemaModalLabel').text('CUIDADO: Faltan las coordenadas');
        $('#descripcionProblema').text('Señala un punto en el mapa.');
        $('#problemaModal').modal();
        return;
    } else if ($("#FECHA").val() == "") {
        $('#problemaModalLabel').text('CUIDADO: Falta la fecha');
        $('#descripcionProblema').text('Selecciona una fecha.');
        $('#problemaModal').modal();
        return;
    } else {
        $("#dataform").submit();
        return;
    }
    return;
}


// Comprueba la existencia o no del IDColor al pulsar en el boton
function compruebaIDColor() {
    var idcolor = $('#IDCOLOR').val()
    if (idcolor == "") {
        $('#problemaModalLabel').text('CUIDADO: Falta IDColor');
        $('#descripcionProblema').text('Por favor, introduce un valor en el campo IDColor para comprobar su existencia.');
        $('#problemaModal').modal();
    } else {
        console.log("Comprobando IDColor");
    }
}