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
define(['ojs/ojcore', 'knockout',
        'appController',
        'appUtils',
        'ojs/ojknockout',
        'ojs/ojarraytabledatasource',
        'ojs/ojradioset'],
function(oj, ko, app, appUtils) {
  function priority(params) {
    var self = this;
    self.incidentData = params.incidentData;
    self.priorityChange = params.priorityChange;
    self.isReadOnlyMode = app.isReadOnlyMode;

    self.connected = function() {
      appUtils.adjustContentPadding();
    }

    var priorityOptionsArr = [{'id': 'high', 'title': 'High'},
                              {'id': 'normal', 'title': 'Normal'},
                              {'id': 'low', 'title': 'Low'}];

    self.priorityOptions= ko.observableArray();
    self.priorityOptions(new oj.ArrayTableDataSource(priorityOptionsArr, {idAttribute: 'id'}));

  }

  return priority;
});
