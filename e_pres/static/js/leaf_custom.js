L.NumberedDivIcon = L.Icon.extend({
options: {
iconUrl: '../static/img/raspi.png',
number: '',
shadowUrl: null,
iconSize: new L.Point(25, 41),
iconAnchor: new L.Point(12, 41),
//popupAnchor: new L.Point(0, -33),
/*
iconAnchor: (Point)
popupAnchor: (Point)
*/
className: 'leaflet-div-icon'
},

createIcon: function () {
var div = document.createElement('div');
var img = this._createImg(this.options['iconUrl']);
var numdiv = document.createElement('div');
numdiv.setAttribute ( "class", "number" );
numdiv.innerHTML = this.options['number'] || '';
div.appendChild ( img );
div.appendChild ( numdiv );
this._setIconStyles(div, 'icon');
return div;
},

//you could change this to add a shadow like in the normal marker if you really wanted
createShadow: function () {
return null;
}
});


// create the slippy map
var map = L.map('image-map', {
  minZoom: 2,
  maxZoom: 4,
  center: [-75, 102],
  zoom: 1,
  crs: L.CRS.Simple
});




// dimensions of the image
var w = 1754,
    h = 1240,
    url = '../static/img/blueprint.jpg';

// calculate the edges of the image, in coordinate space
var southWest = map.unproject([0, h], map.getMaxZoom()-1);
var northEast = map.unproject([w, 0], map.getMaxZoom()-1);
var bounds = new L.LatLngBounds(southWest, northEast);

// add the image overlay,
// so that it covers the entire map
L.imageOverlay(url, bounds).addTo(map);




// tell leaflet that the map is exactly as big as the image
map.setMaxBounds(bounds);




// var planes = [
// ["id:10",-72.625, 38.125],
// ["id:20",-73.125, 107.75],
// ["id:30",-81.125, 26.125],
// ["id:40",-102.625, 109.875],
// ["id:50",-82.125, 104.875],
// ["id:60",-79.875, 127.125],
// ["id:70",-71.875, 149.375],
// ["id:80",-80.75, 160.625],
// ["id:90",-65.875, 168.75]
// ];
//
// for (var i = 0; i < planes.length; i++) {
// marker = new L.marker([planes[i][1],planes[i][2]], {icon: new L.NumberedDivIcon({number: planes[i][0]})}).addTo(map);
// }
