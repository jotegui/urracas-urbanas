var coordsTaconera = [
    new google.maps.LatLng(42.81882, -1.6511),
    new google.maps.LatLng(42.81914, -1.65172),
    new google.maps.LatLng(42.81933, -1.65277),
    new google.maps.LatLng(42.81918, -1.65537),
    new google.maps.LatLng(42.8191, -1.65571),
    new google.maps.LatLng(42.81891, -1.65588),
    new google.maps.LatLng(42.81873, -1.65594),
    new google.maps.LatLng(42.81646, -1.65476),
    new google.maps.LatLng(42.81549, -1.65447),
    new google.maps.LatLng(42.81529, -1.65406),
    //new google.maps.LatLng(42.81502, -1.65399),
    //new google.maps.LatLng(42.81464, -1.65279),
    new google.maps.LatLng(42.81571, -1.65108), // new
    new google.maps.LatLng(42.81682, -1.64963),
    new google.maps.LatLng(42.81767, -1.65052)
];
  
var coordsCampus = [
    new google.maps.LatLng(42.80534, -1.6622),
    new google.maps.LatLng(42.80124, -1.66863),
    new google.maps.LatLng(42.80114, -1.66758),
    new google.maps.LatLng(42.80049, -1.66733),
    new google.maps.LatLng(42.80049, -1.66672),
    new google.maps.LatLng(42.79972, -1.66671),
    new google.maps.LatLng(42.79905, -1.66416),
    new google.maps.LatLng(42.79812, -1.66214),
    new google.maps.LatLng(42.79897, -1.66152),
    new google.maps.LatLng(42.79898, -1.66112),
    new google.maps.LatLng(42.79803, -1.6606),
    new google.maps.LatLng(42.79818, -1.66004),
    new google.maps.LatLng(42.7958, -1.65519),
    new google.maps.LatLng(42.79568, -1.65211),
    new google.maps.LatLng(42.7966, -1.65235),
    new google.maps.LatLng(42.79706, -1.65197),
    new google.maps.LatLng(42.79644, -1.65112),
    new google.maps.LatLng(42.79675, -1.64903),
    new google.maps.LatLng(42.7972, -1.64821),
    new google.maps.LatLng(42.79702, -1.64755),
    new google.maps.LatLng(42.7973, -1.6464),
    new google.maps.LatLng(42.80098, -1.64917),
    new google.maps.LatLng(42.8021, -1.65057),
    new google.maps.LatLng(42.80335, -1.65523),
    new google.maps.LatLng(42.80346, -1.65608),
    new google.maps.LatLng(42.8039, -1.65653),
    new google.maps.LatLng(42.80449, -1.65846)
];
  
coordsCastanos = [
    new google.maps.LatLng(42.80406, -1.66431), // Inicio Entrada
    new google.maps.LatLng(42.80463, -1.66379),
    new google.maps.LatLng(42.80484, -1.66383),
    new google.maps.LatLng(42.80495, -1.66405),
    new google.maps.LatLng(42.80482, -1.66436),
    new google.maps.LatLng(42.80473, -1.66418),
    new google.maps.LatLng(42.80454, -1.66401),
    new google.maps.LatLng(42.80444, -1.66402),
    new google.maps.LatLng(42.80439, -1.66422),
    new google.maps.LatLng(42.80425, -1.66419),
    new google.maps.LatLng(42.80409, -1.66434), // Fin Entrada
    new google.maps.LatLng(42.80404, -1.66464),
    new google.maps.LatLng(42.80393, -1.66462),
    new google.maps.LatLng(42.80389, -1.66469),
    new google.maps.LatLng(42.80391, -1.66483),
    new google.maps.LatLng(42.80375, -1.66495),
    new google.maps.LatLng(42.80378, -1.66514),
    new google.maps.LatLng(42.80399, -1.6651),
    new google.maps.LatLng(42.80406, -1.66524), // Esquina paso transiberiano
    new google.maps.LatLng(42.80405, -1.66532), // Esquina paso transiberiano
    new google.maps.LatLng(42.80374, -1.66588),
    new google.maps.LatLng(42.80337, -1.66555),
    new google.maps.LatLng(42.80309, -1.66617),
    new google.maps.LatLng(42.80331, -1.66644),
    new google.maps.LatLng(42.80312, -1.66684),
    new google.maps.LatLng(42.80268, -1.66655)
];
  
var coordsCiudadela = [
    //new google.maps.LatLng(42.81491, -1.65422),
    //new google.maps.LatLng(42.81448, -1.65457),
    new google.maps.LatLng(42.81415, -1.65288), // new
    new google.maps.LatLng(42.81289, -1.6542), // new
    new google.maps.LatLng(42.81207, -1.65442),
    new google.maps.LatLng(42.81005, -1.65324),
    new google.maps.LatLng(42.80938, -1.65221),
    new google.maps.LatLng(42.80866, -1.64986),
    new google.maps.LatLng(42.80869, -1.64819),
    new google.maps.LatLng(42.8096, -1.64582),
    new google.maps.LatLng(42.80961, -1.64525),
    new google.maps.LatLng(42.81038, -1.64479),
    new google.maps.LatLng(42.81248, -1.64582),
    new google.maps.LatLng(42.81433, -1.65265)
];
  
var areaTaconera = new google.maps.Polygon({
    paths: coordsTaconera,
    strokeColor: 'white',
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: 'white',
    fillOpacity: 0.3,
    zIndex: 2
});
  
var areaCampus = new google.maps.Polygon({
    paths: coordsCampus,
    strokeColor: 'orange',
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: 'orange',
    fillOpacity: 0.3,
    zIndex: 2
});
  
var areaCastanos = new google.maps.Polygon({
    paths: coordsCastanos,
    strokeColor: 'orange',
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: 'orange',
    fillOpacity: 0.3,
    zIndex: 2
});
  
var areaCiudadela = new google.maps.Polygon({
    paths: coordsCiudadela,
    strokeColor: 'yellow',
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: 'yellow',
    fillOpacity: 0.3,
    zIndex: 2
});