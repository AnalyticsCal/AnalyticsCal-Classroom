/**
 * @license
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
/**
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
'use strict';
define(['appUtils', 'ojs/ojradioset', 'ojs/ojknockout'], function(appUtils) {
  function createIncident_contact(params) {
    var self = this;
    self.appUtilities = appUtils;

    self.prefetch = function() {
      self.allCustomers = params.allCustomers;
      self.newIncidentModel = params.newIncidentModel;
      self.customerSelectionChange = params.customerSelectionChange;
    }

    self.connected = function() {
      // With caching enabled, the radio has to be refreshed
      // when this VM is restored from cache. Otherwise the layout
      // of the radio goes for a toss.
      var radio = document.getElementById('customerSelectionRadioSet');
      oj.Context.getContext(radio).getBusyContext().whenReady().then(function () {
        radio.refresh();
      });
    }
  }

  return createIncident_contact;

});
