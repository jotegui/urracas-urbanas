function initialize() {}

function initializeObsMap(lat, lng) {
  
  if (lat == 0) {
    lat=42.8156;
  }
  if (lng == 0) {
    lng=-1.6454;
  }
  
  var latlng = new google.maps.LatLng(lat, lng)
  var mapOptions = {
    center: latlng,
    zoom: 16,
    mapTypeId: google.maps.MapTypeId.SATELLITE,
    tilt:0
  };
  var map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
  var center = map.getCenter();
  $('#mapaNidos').on('shown.bs.modal', function () {
    google.maps.event.trigger(map, "resize");
    map.setCenter(center);
  });
  
  marker = createMarker(latlng, map);
  
}