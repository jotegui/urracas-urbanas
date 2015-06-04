function initialize() {initializeMap(42.81211, -1.64922);}

function initializeMap(lat, lng) {
  
  if (lat == 0) {
    lat=42.8156;
  }
  if (lng == 0) {
    lng=-1.6454;
  }
  var mapOptions = {
    center: new google.maps.LatLng(lat, lng),
    zoom: 16,
    mapTypeId: google.maps.MapTypeId.SATELLITE,
    tilt:0
  };
  var map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
  /*var center = map.getCenter();
  $('#mapaNidos').on('shown.bs.modal', function () {
    google.maps.event.trigger(map, "resize");
    map.setCenter(center);
    $("#submitnido").prop("disabled", true);
  });*/
  
  google.maps.event.addListener(map, 'click', function(event) {
    if (marker) {
      marker.setMap(null);
      marker = null;
    }


    if ($("#submitnido").prop("disabled")) {
      $("#submitnido").prop("disabled", false);
    }

    marker = createMarker(event.latLng, map);
    $("#lat").val(Math.round(event.latLng.lat()*100000)/100000);
	$("#lng").val(Math.round(event.latLng.lng()*100000)/100000);
  });
  
}