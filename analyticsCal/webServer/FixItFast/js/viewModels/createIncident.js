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
        'mapping',
        'dataService',
        'appController',
        'ModuleHelper',
        'ImageHelper',
        'appUtils',
        'ojs/ojmodule-element',
        'ojs/ojknockout',
        'ojs/ojtrain',
        'ojs/ojarraytabledatasource'],
function(oj, ko, mapping, data, app, moduleHelper, imageHelper, appUtils) {
  function createIncident(params) {
    ko.mapping = mapping;
    var allCustomers = ko.observableArray();
    var customersDataSource = new oj.ArrayTableDataSource(allCustomers, {idAttribute: "id"});
    var initialLoad = true;

    var newIncidentObj = {
      "problem": "",
      "category": "general",
      "picture": "",
      "priority": "high",
      "customerId": "",
      "locationId": "",
      "customerName": ""
    };

    var newIncidentModel = ko.observable(ko.mapping.fromJS(newIncidentObj));

    var routerConfig = {
      'createIncident_problem': { label: 'Problem', isDefault: true, value: {prev:'Cancel', next: 'Next', showTrain: true } },
      'createIncident_photo': { label: 'Photo', value: {prev:'Previous', next: 'Next', showTrain: true } },
      'createIncident_contact': { label: 'Contact', value: {prev:'Previous', next: 'Next', showTrain: true } },
      'createIncident_summary': { label: 'Summary', value: {prev:'Previous', next: 'Submit', showTrain: true } },
      'createIncident_submit': { label: 'Submit', value: {prev:'', next: '', showTrain: false } }
    };

    var self = this;
    self.stepArray = ko.observableArray();
    self.router = params.parentRouter.createChildRouter('createIncident').configure(routerConfig);
    self.router.trainStepDirection = 'next';

    // This is to prevent direct navigation to any views other than the starting one.
    self.router.stateId.subscribe(function(newValue) {
      if (initialLoad && newValue !== 'createIncident_problem')
        self.router.go('createIncident_problem', { historyUpdate: 'skip' });
    });


    for (var key in routerConfig) {
      if (key === 'createIncident_submit')
        continue;
      self.stepArray.push({
        id: key,
        label: routerConfig[key].label
      })
    }


    self.prefetch = function() {
      return new Promise(function(resolve, reject) {
        data.getCustomers().then(function(response) {
          var result = JSON.parse(response).result;

          // sort by firstName then lastName within each group
          result.sort(function(a, b) {
            // sort by first name
            if (a.firstName.toLowerCase() > b.firstName.toLowerCase())
              return 1;
            else if (a.firstName.toLowerCase() < b.firstName.toLowerCase())
              return -1;

            // else sort by last name
            return (a.lastName.toLowerCase() > b.lastName.toLowerCase()) ? 1 : (a.lastName.toLowerCase() < b.lastName.toLowerCase()) ? -1 : 0;
          });

          allCustomers(result);
          customersDataSource = new oj.ArrayTableDataSource(allCustomers, {idAttribute: "id"});
          resolve();
        });
      })
    }

    self.connected = function() {
      appUtils.adjustContentPadding();
      oj.Router.sync();
      self.train = document.getElementById('train');
    };

    self.transitionCompleted = function() {
      // adjust content padding top
      var train = document.getElementById('train');
      oj.Context.getContext(train).getBusyContext().whenReady().then(function () {
        appUtils.adjustContentPadding();
      });
    };

    // dispose create incident page child router
    self.disconnected = function() {
      delete self.train;
      self.router.dispose();
    };

    // Validate required fields
    self._validateRequiredFields = function (pageId) {
      var incident = ko.mapping.toJS(newIncidentModel);
      if (pageId == "createIncident_problem") {
        if (!incident.problem) {
          // Custom Error Message
          document.getElementById('problem-input').messagesCustom = [new oj.Message('Required.', 'Please describe the problem.')];
          return false;
        }
        else if (!document.getElementById("categoryRadioSet").validate())
          return false;
        else if (!document.getElementById("priorityRadioSet").validate())
          return false;
      }
      else if (pageId == "createIncident_contact") {
        if (!incident.customerId) {
          // Custom Error Message
          document.getElementById("customerSelectionRadioSet").messagesCustom = [new oj.Message('Required.', 'Please select a customer.')];
          return false;
        }
      }
      return true;
    }

    // go to next step
    function nextStep() {
      var next = self.train.getNextSelectableStep();
      self.router.trainStepDirection = 'next';

      if (next === null) {
        submitIncident();
        return;
      }

      if (!self._validateRequiredFields(train.selectedStep))
        return;

      initialLoad = false;
      self.router.go(next, { historyUpdate: 'skip' });
    };

    // go to previous step
    function previousStep() {
      if (!self.router.currentValue())
        return;

      // This is for the submit success page case.
      // Although it is shown only for few seconds, user can potentially click on the hamburger menu
      if (!self.router.currentValue().showTrain) {
        app.toggleDrawer();
        return;
      }

      var prev = self.train.getPreviousSelectableStep();
      self.router.trainStepDirection = 'previous';

      initialLoad = false;
      if (prev !== null) {
        self.router.go(prev, { historyUpdate: 'skip' });
        return;
      }

      // This is for the case where user wants to abort creating an incident.
      app.goToIncidents();
    };

    self.trainBeforeSelect = function (event) {
      if (!event.detail.originalEvent || !event.detail.toStep)
        return;

      // router takes care of changing the selection
      event.preventDefault();

      // If validation fails, prevent navigation.
      if (event.detail.fromStep && !self._validateRequiredFields(event.detail.fromStep.id))
        return false;

      var steps = self.stepArray();
      for (var i = 0; i < steps.length; i++) {
        switch (steps[i].id) {
          // If first one found is the from, going forward
          case event.detail.fromStep.id:
            self.router.trainStepDirection =  'next';
            i = steps.length;
            break;

          // If first one found is the to, going backward
          case event.detail.toStep.id:
            self.router.trainStepDirection =  'previous';
            i = steps.length;
            break;
        }
      }

      initialLoad = false;
      self.router.go(event.detail.toStep.id, { historyUpdate: 'skip' });
    }

    function finishIncidentCreate(timeout, err) {
      var errMsg;
      if (err) {
        errMsg = 'Failed to create incident.';
        oj.Logger.error(errMsg, err);
      }
      app.connectionDrawer.showAfterUpdateMessage(errMsg);
      if (timeout > 0 ) {
        setTimeout(function() {
          app.goToIncidents();
        }, timeout);
      } else {
        app.goToIncidents();
      }
    }

    // submit new incident
    function submitIncident() {
      var incident = ko.mapping.toJS(newIncidentModel);
      delete incident.customerName;
      incident.customerId = incident.customerId;

      // TODO validation
      if (!incident.problem) {
        app.router.go("createIncident");
        return oj.Logger.warn('Please enter the problem');
      }

      if (!incident.customerId) {
        app.router.go("createIncident/createIncident_contact");
        return oj.Logger.warn('Please select a customer');
      }

      // if image is in url, convert to base64
      imageHelper.loadImage(incident.picture)
        .then(function(imgData) {
          incident.picture = imgData;
          self.router.go('createIncident_submit');
          return data.createIncident(incident);
        })
        .then(function(response){
          // go back to incidents list after 1.5s
          finishIncidentCreate(1500);
        })
        .catch(function(err) {
          finishIncidentCreate(0, err);
        });
    };

    var icons = ko.computed(function() {
      if(self.router.currentValue())
        if(self.router.currentValue().showTrain) {
          return 'oj-hybrid-applayout-header-icon-back demo-icon oj-fwk-icon';
        } else {
          return 'oj-fwk-icon oj-fwk-icon-hamburger oj-button-icon oj-start';
        }
      else
        return 'oj-fwk-icon oj-fwk-icon-hamburger oj-button-icon oj-start';

    });

    var disableSubmit = ko.computed(function() {
      return self.router.stateId() === 'createIncident_summary' && app.isReadOnlyMode;
    });

    var submitVisible = ko.computed(function(){
      return self.router.currentValue() ? self.router.currentValue().showTrain : false;
    });

    var submitLabel = ko.computed(function(){
      return self.router.currentValue() ? self.router.currentValue().next : '';
    });

    var backLabel = ko.computed(function(){
      return self.router.currentValue() ? self.router.currentValue().prev : '';
    });

    // setup header moduleConfig
    var headerViewModelParams = {
      title: 'New Incident',
      startBtn: {
        id: 'backBtn',
        click: previousStep,
        display: 'icons',
        label: backLabel,
        icons: icons,
        visible: true
      },
      endBtn: {
        id: 'nextBtn',
        click: nextStep,
        display: 'icons',
        label: submitLabel,
        icons: 'oj-fwk-icon oj-fwk-icon-next',
        visible: submitVisible,
        disabled: disableSubmit
      }
    };

    moduleHelper.setupStaticModule(self, 'createIncidentHeaderConfig', 'basicHeader', headerViewModelParams);

    // handler when customer selection changes
    function customerSelectionChange(event) {
      var value = event.detail.value;
      if(value) {

        var selectedCustomer = allCustomers().filter(function(customer) {
          return customer.id === value;
        });

        newIncidentModel().customerName(selectedCustomer[0].firstName + ' ' + selectedCustomer[0].lastName);
        newIncidentModel().locationId(selectedCustomer[0].locationId);
      }
    };

    // setup moduleConfig
    var moduleParams = {
      'parentRouter': self.router,
      'newIncidentModel': newIncidentModel,
      'allCustomers': allCustomers,
      'customerSelectionChange': customerSelectionChange,
    };

    moduleHelper.setupModuleCaching(self);
    moduleHelper.setupModuleWithObservable(self, 'moduleConfig', self.router.stateId, moduleParams);
  }

  return createIncident;

});
