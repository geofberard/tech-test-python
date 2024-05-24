function displayMap(points) {
  var map = new ol.Map({
    target: 'roadtrip-map',
    layers: [new ol.layer.Tile({ source: new ol.source.OSM() })],
    view: new ol.View({ center: ol.proj.fromLonLat([-96, 37.0902]), zoom: 4 })
  });

  var vectorSourcePoints = new ol.source.Vector();

  var vectorLayerPoints = new ol.layer.Vector({
    source: vectorSourcePoints,
    style: new ol.style.Style({
      image: new ol.style.Circle({ radius: 4, fill: new ol.style.Fill({ color: 'DodgerBlue' }), })
    })
  });
  map.addLayer(vectorLayerPoints);

  points.forEach(function (point) {
    var marker = new ol.Feature({
      geometry: new ol.geom.Point(ol.proj.fromLonLat([point.longitude, point.latitude]))
    });
    vectorSourcePoints.addFeature(marker);
  });

  // Couche pour les lignes
  var lineString = new ol.geom.LineString(points.map(function (point) {
    return ol.proj.fromLonLat([point.longitude, point.latitude]);
  }));

  var featureLine = new ol.Feature({ geometry: lineString });
  var vectorSourceLine = new ol.source.Vector({ features: [featureLine] });
  var vectorLayerLine = new ol.layer.Vector({
    source: vectorSourceLine,
    style: new ol.style.Style({
      stroke: new ol.style.Stroke({ color: 'DodgerBlue', width: 2 })
    })
  });
  map.addLayer(vectorLayerLine);
}