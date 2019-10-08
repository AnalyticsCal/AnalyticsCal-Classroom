/**
 * @license
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
/**
 * @license
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
'use strict';
define(['ojs/ojcore', 'knockout', 'jquery',
        'dataService',
        'appController',
        'ModuleHelper',
        'ojs/ojknockout',
        'oraclemapviewer',
        'oracleelocation'], function(oj, ko, $, data, app, moduleHelper) {
  function customerLocationMap(params) {

    var self = this;
    self.customerData = ko.observable(params);

    self.prefetch = function() {
      // TODO: find if we can wait for map to load.
      return Promise.resolve();
    }

    self.connected = function() {
      // adjust padding for details panel
      var topElem = document.getElementsByClassName('oj-applayout-fixed-top')[0];

      if (topElem) {
        $('#detailsPanel').css('padding-top', topElem.offsetHeight+'px');
      }

      // dismiss details panel when click on map
      $('#map').on('click touchstart', function() {
        $('#detailsPanel').slideUp();
      })
    }

    self.locationId = self.customerData().locationId;

    self.map = ko.observable({
      customerLocation: ko.observable()
    });

    // load customer location data
    function updateLocationData() {
      self.map().customerLocation({
        lat: self.customerData().address.latitude(),
        lng: self.customerData().address.longitude()
      });
    }

    self.locationId.subscribe(function(newValue) {
      if(newValue) {
        updateLocationData();
      }
    });

    ko.bindingHandlers.customerLocMap = {

      init: function (element, valueAccessor, allBindingsAccessor, viewModel) {
        var mapObj = ko.utils.unwrapObservable(valueAccessor());

        mapObj._hasCustomerLoc = ko.observable(false);

        mapObj.onChangedCustomerLoc = function(newValue) {
          /* Oracle mapViewer code start */
          OM.gv.setLogLevel('severe');
          var eloc = new OracleELocation();
          OM.gv.setResourcePath("https://elocation.oracle.com/mapviewer/jslib/v2.1");
          mapObj.map = new OM.Map(element, {mapviewerURL: ''}) ;
          var tileLayer = new OM.layer.OSMTileLayer("layer1");
          mapObj.map.addLayer(tileLayer);
          var markerLayer = new OM.layer.MarkerLayer("markerlayer1");
          markerLayer.setBoundingTheme(true);
          mapObj.map.addLayer(markerLayer);

          mapObj.customerLatLng = { lon: newValue.lng, lat: newValue.lat };

          var vMarker = new OM.style.Marker({
            src: "css/images/alta_map_pin_red.png",
            width: 17,
            height: 36,
            lengthUnit: 'pixel'
          })
          var mm = new OM.MapMarker();
          markerLayer.addMapMarker(mm);
          mm.setPosition(newValue.lng, newValue.lat);
          mm.setDraggable(false);
          mm.setStyle(vMarker);
          mm.setID('customerLocation');
          mm.on('click', function(click) {
            // prevent propagation to map
            click.evt.stopPropagation();
            $("#detailsPanel").slideToggle();
          });

          mapObj.map.init();
          return mapObj._hasCustomerLoc(true);

        };

        if(mapObj.locationSubscription) {
          mapObj.locationSubscription.dispose();
        }
        mapObj.locationSubscription = mapObj.customerLocation.subscribe(mapObj.onChangedCustomerLoc);

        if (self.locationId()) {
          updateLocationData();
        }
        $("#" + element.getAttribute("id")).data("mapObj", mapObj);
      }
    };


    self.duration = ko.observable();
    self.distance = ko.observable();

    self.showDetails = function() {
      $("#detailsPanel").slideToggle();
    };

  }

  return customerLocationMap;
});
