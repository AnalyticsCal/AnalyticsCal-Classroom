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
        'dataService',
        'ModuleHelper',
        'ImageHelper',
        'appUtils',
        'ojs/ojmodule-element',
        'ojs/ojknockout',
        'ojs/ojvalidationgroup',
        'ojs/ojformlayout',
        'ojs/ojinputtext'],
function(oj, ko, app, data, moduleHelper, imageHelper, appUtils) {
  function customerCreate(params) {
    var self = this;

    self.prefetch = function() {
      self.customer = {
        firstName: ko.observable(),
        lastName: ko.observable(),
        mobile: ko.observable(),
        home: ko.observable(),
        email: ko.observable(),
        photo: ko.observable(), // Photo is not supported by backend yet.
        address: ko.observable({
          street1: ko.observable(),
          street2: ko.observable(),
          city: ko.observable(),
          state: ko.observable(),
          zip: ko.observable(),
          country: ko.observable()
        })
      };
      self.groupValid = ko.observable();
      self.imgSrc = ko.observable('css/images/Add_avatar@2x.png');
    }

    self.connected = function() {
      appUtils.adjustContentPadding();
      imageHelper.registerImageListeners(app, 'upload-new-customer-pic', self.imgSrc, self, 'changePhoto');
    };

    // create new customer
    self.createCustomer = function() {
      document.getElementById("addFirstNameInput").validate();
      document.getElementById("addLastNameInput").validate();
      var tracker = document.getElementById("tracker");
      if (tracker.valid !== "valid") {
        return;
      }

      imageHelper.loadImage(self.imgSrc())
        .then(function(base64Image) {
          self.customer.photo(base64Image); // Photo is not supported at backend yet.
          return data.createCustomer(ko.toJS(self.customer));
        })
        .then(function(response){
          var result = JSON.parse(response);
          app.goToCustomer(result.id);
          app.connectionDrawer.showAfterUpdateMessage();
        })
        .catch(function(err) {
          var errMsg = 'Failed to create customer.';
          oj.Logger.error(errMsg, err);
          app.goToCustomers();
          app.connectionDrawer.showAfterUpdateMessage(errMsg);
        });
    };

    // go to previous page
    self.goToPrevious = function() {
      window.history.back();
    };

    // create customer page header settings
    var headerViewModelParams = {
      title: 'Add Customer',
      startBtn: {
        id: 'backBtn',
        click: self.goToPrevious,
        display: 'icons',
        label: 'Back',
        icons: 'oj-hybrid-applayout-header-icon-back oj-fwk-icon',
        visible: true
      },
      endBtn: {
        id: 'saveBtn',
        click: self.createCustomer,
        display: 'all',
        label: 'Save',
        icons: '',
        visible: true,
        disabled: app.isReadOnlyMode
      }
    };

    moduleHelper.setupStaticModule(self, 'custAddHeaderConfig', 'basicHeader', headerViewModelParams);
  }

  return customerCreate;
});
