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
        'dataService', 'appController', 'ModuleHelper',
        'ojs/ojmodule-element', 'ojs/ojknockout'], function(oj, ko, data, app, moduleHelper) {
  function incident(params) {
    var self = this;

    self.incidentData = ko.observable();
    self.moduleConfig = ko.observable();

    var refreshIncident = function (response) {
      var incidentData = JSON.parse(response.detail);
      incidentData.statusSelection = ko.observableArray([incidentData.status]);
      incidentData.prioritySelection = ko.observableArray([incidentData.priority]);
      self.incidentData(incidentData);
    };

    var parentRouter = params.parentRouter;

    function loadModule() {
      var moduleParams = {
        'locationId':self.locationId,
        'parentRouter': self.router,
        'incidentData': self.incidentData,
        'priorityChange': self.priorityChange,
        'statusChange': self.statusChange
      };

      moduleHelper.setupStaticModule(self, 'moduleConfig', 'incidentViews', moduleParams);
    }

    self.prefetch = function() {
      return new Promise(function(resolve, reject) {
        self.router = parentRouter.createChildRouter('incident').configure(function(stateId) {
          if(stateId) {
            if (self.routerState && self.routerState.id == stateId)
              return self.routerState;

            self.routerState = new oj.RouterState(stateId, {
              canEnter: function () {
                return data.getIncident(stateId).then(function(response) {
                  var incidentData = JSON.parse(response);
                  incidentData.statusSelection = ko.observableArray([incidentData.status]);
                  incidentData.prioritySelection = ko.observableArray([incidentData.priority]);
                  self.incidentData(incidentData);
                  loadModule();
                  resolve();
                  return true;
                });
              }
            });
            return self.routerState;
          }
        });

        oj.Router.sync();
      });
    }

    self.disconnected = function() {
      document.getElementById('page').removeEventListener('onIncidentUpdated', refreshIncident);
      self.router.dispose();
      self.routerState = undefined;
    };

    self.connected = function() {
      document.getElementById('page').addEventListener('onIncidentUpdated', refreshIncident);
    }

    self.locationId = ko.computed(function() {
      if (self.incidentData()) {
        return self.incidentData().locationId;
      }
    });


    // update incident when status or priority changes
    self.updateIncident = function(id, incident) {
      data.updateIncident(id, incident).then(function(response){
        // update success
      }).fail(function(response) {
        oj.Logger.error('Failed to update incident.', response);
        app.connectionDrawer.showAfterUpdateMessage();
      });
    };

    // priority selection change
    self.priorityChange = function(event) {
      updatePriorityStatus('priority', event);
    };

    // status selection change
    self.statusChange = function(event) {
      updatePriorityStatus('status', event);
    };

    function updatePriorityStatus(option, event) {
      var value = event.detail.value;
      if(value) {
        var incident = {};
        incident[option] = value;
        self.updateIncident(self.router.stateId(), incident);
      }
    };
  }

  return incident;

});
