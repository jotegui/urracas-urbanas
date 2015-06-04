/*
function activarModif(ele) {
    
    if ($(ele).prop('checked') == true) {
        $('#'+$(ele).attr('id')+'val').prop('disabled', false);
    } else {
        $('#'+$(ele).attr('id')+'val').prop('disabled', true);
    }
}
*/

$(function() {
    // Activar todos los tooltips
    // Enlaces de info
    $('.enlaceave').tooltip({delay: { "show": 2000 }});  
    // Enlace de salida
    $('#exitlink').tooltip();
    // Enlace de ayuda
    $('#helplink').tooltip();

    // Activar los switches
    $('[data-toggle="popover"]').popover();
    
    // Activar los checkboxes
     $('.formcheckbox').bootstrapSwitch({
        size: "normal",
        onText: "Sí",
        offText: "No"
    });

});

compruebaRelacion = function() {
    if ($("#sujeto").val() == $('#objeto').val()) {
        $('#problemaModalLabel').text('CUIDADO');
        $('#descripcionProblema').text('Una urraca no puede estar relacionada consigo misma.');
        $('#problemaModal').modal();
        return;
    } else {
        $("#parentescoForm").submit();
        return;
    }
}