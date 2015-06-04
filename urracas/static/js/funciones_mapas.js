var map = null;
var marker = null;

function exportCoordinates(event) {
	 if (marker) {
	    marker.setMap(null);
	    marker = null;
	 }
	 marker = createMarker(event.latLng, map);
	 $("#lat").val(Math.round(event.latLng.lat()*100000)/100000);
	 $("#lng").val(Math.round(event.latLng.lng()*100000)/100000);
  }

function createMarker(latlng, mapsel) {
    var marker = new google.maps.Marker({
        position: latlng,
        map: mapsel,
        zIndex: Math.round(latlng.lat()*-100000)<<5,
        animation: google.maps.Animation.DROP
        });
   
    return marker;
}