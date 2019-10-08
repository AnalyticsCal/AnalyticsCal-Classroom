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
        'ojs/ojarraytabledatasource',
        'ojs/ojradioset'],
function(oj, ko, app, appUtils) {
  function status(params) {
    var self = this;
    self.incidentData = params.incidentData;
    self.statusChange = params.statusChange;
    self.isReadOnlyMode = app.isReadOnlyMode;

    self.connected = function() {
      appUtils.adjustContentPadding();
    };

    var statusOptionsArr = [{'id': 'open', 'title': 'Open'},
                            {'id': 'accepted', 'title': 'Accepted'},
                            {'id': 'closed', 'title': 'Closed'}];

    self.statusOptions = ko.observableArray();
    self.statusOptions(new oj.ArrayTableDataSource(statusOptionsArr, {idAttribute: 'id'}));
  }

  return status;
});
