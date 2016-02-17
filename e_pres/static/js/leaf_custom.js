
L.NumberedDivIcon = L.Icon.extend({
    options: {
      iconUrl: '/static/img/raspi.png',
      number: '',
      shadowUrl: null,
      iconSize: new L.Point(25, 41),
      iconAnchor: new L.Point(12, 41),
      className: 'leaflet-div-icon'
    },
    createIcon:
      function () {
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
    createShadow:
      function () {
        return null;
      }
    });


  function defineMap(id){
    return L.map(id, {
      minZoom: 0,
      maxZoom: 4,
      center: [-75, 102],
      zoom: 1,
      crs: L.CRS.Simple
    });
  };


  function setMap(map, w, h, url){
    var southWest = map.unproject([0, h], map.getMaxZoom()-1);
    var northEast = map.unproject([w, 0], map.getMaxZoom()-1);
    var bounds = new L.LatLngBounds(southWest, northEast);

    L.imageOverlay(url, bounds).addTo(map);
    map.setMaxBounds(bounds);
    map.on('click', onMapClick);
  };
