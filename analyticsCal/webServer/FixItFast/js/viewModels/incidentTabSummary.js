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
define(['knockout', 'appUtils', 'ojs/ojknockout', 'ojs/ojlistview'], function(ko, appUtils) {
  function incidentTabSummary(params) {
    var self = this;
    self.goToPriority = params.goToPriority;
    self.goToStatus = params.goToStatus;
    self.goToCustomer = params.goToCustomer;
    self.incidentData = params.incidentData;
    self.mapHref = ko.observable();
    self.goToCustomerLocationMap = params.goToCustomerLocationMap;

    self.prefetch = function() {
      // Data is passed as parameter. No new data to load
      return Promise.resolve();
    }

    // adjust content padding top
    self.connected = function() {
      appUtils.adjustContentPadding();
      self.mapHref(appUtils.getMapPrefix() + '0,0?q=' + self.incidentData().location.formattedAddress);
    };

    // trigger click when selection changes
    self.optionChange = function (event) {
      var detail = event.detail;
      if(detail.items && detail.items[0]) {
        detail.items[0].click();
      }
    };

  }

  return incidentTabSummary;
});
