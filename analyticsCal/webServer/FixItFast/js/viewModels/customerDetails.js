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
define(['ojs/ojcore', 'knockout',
        'dataService',
        'appController',
        'mapping',
        'ModuleHelper',
        'ImageHelper',
        'appUtils',
        'ojs/ojmodule-element',
        'ojs/ojknockout',
        'ojs/ojvalidationgroup',
        'ojs/ojinputtext',
        'ojs/ojlabel',
        'ojs/ojformlayout'],
function(oj, ko, data, app, mapping, moduleHelper, imageHelper, appUtils) {
  function customerDetails(params) {
    ko.mapping = mapping;

    var self = this;
    self.appUtilities = appUtils;
    self.parentRouter = params.parentRouter;
    self.editMode = ko.observable(false);
    self.imgSrc = ko.observable();
    self.customerModel = ko.observable();
    self.mapHref = ko.observable();
    self.contactUpdateSummary = ko.observable();
    self.contactUpdateDetail = ko.observable();
    self.customerHasAddress = ko.observable(false);
    self.groupValid = ko.observable();
    self.customerLocationMapVisible = ko.observable(false);

    var refreshCustomer = function (response) {
      self.customerData = JSON.parse(response.detail);
      if(self.customerData) {
        self.customerModel(ko.mapping.fromJS(self.customerData));
        self.initialData = self.customerData;
      }
    }

    self.prefetch = function() {
      return new Promise(function(resolve, reject) {
        self.router = self.parentRouter.createChildRouter('customer').configure(function(stateId) {
          if (stateId) {
            if (self.routerState && self.routerState.id == stateId)
              return self.routerState;

            self.routerState = new oj.RouterState(stateId, { value: stateId,
              // Use "canEnter" instead of "enter" because we want to refresh
              // customerData before changing view.  Otherwise, the details view
              // will be changed during or after animation.
              canEnter: function() {
                // load customer data
                return data.getCustomer(stateId).then(function(response) {
                  self.customerData = JSON.parse(response);
                  self.customerModel(ko.mapping.fromJS(self.customerData));
                  self.initialData = self.customerData;
                  resolve();
                  return true;
                });
              }
            });

            return self.routerState;
          }
        });
        oj.Router.sync();
      })
    }

    self.connected = function() {
      document.getElementById('page').addEventListener('onCustomerUpdated', refreshCustomer);

      appUtils.adjustContentPadding();
      imageHelper.registerImageListeners(app, 'upload-customer-pic', self.imgSrc, self, 'changePhoto');

      var customerAddress = self.customerModel().address;
      self.customerHasAddress(customerAddress && customerAddress.latitude
            && customerAddress.longitude && customerAddress.formattedAddress);

      moduleHelper.setupStaticModule(self, 'mapConfig', 'customerLocationMap', self.customerModel());
    };

    self.disconnected = function() {
      document.getElementById('page').removeEventListener('onCustomerUpdated', refreshCustomer);
      self.router.dispose();
      self.routerState = undefined;
    };


    // update customer data
    // TODO update customer photo
    self.updateCustomerData = function() {
      document.getElementById("customerFirstNameInput").validate();
      document.getElementById("customerLastNameInput").validate();
      var tracker = document.getElementById("tracker");
      if (tracker.valid !== "valid") {
        return;
      }

      imageHelper.loadImage(self.imgSrc())
        .then(function(base64Image) {
          self.customerModel().photo = base64Image; // Photo is not supported by backend yet.
          self.initialData = ko.mapping.toJS(self.customerModel);
          var id = self.router.stateId();
          return data.updateCustomer(id, self.initialData);
        })
        .then(function(response){
          app.connectionDrawer.showAfterUpdateMessage();
        })
        .catch(function(err) {
          oj.Logger.error('Failed to update customer.', err);
        });
    };

    // revert changes to customer
    self.revertCustomerData = function() {
      self.customerModel(ko.mapping.fromJS(self.initialData));
    };

    var leftClickAction = function() {
      if (self.customerLocationMapVisible()) {
        self.customerLocationMapVisible(false);
        return;
      }
      if (self.editMode()) {
        self.revertCustomerData();
        self.editMode(false);
        return;
      }

      app.fromIncidentId !== undefined ?
        app.goToIncidentFromCustomer() :
        app.goToCustomers();
    };

    var rightClickAction = function() {
      if(self.editMode()) {
        self.updateCustomerData();
        self.editMode(false);
      } else {
        self.editMode(true);
      }
    };

    var headerTitle = ko.computed(function() {
      return self.customerLocationMapVisible() ? "Customer Location" : "Customer";
    });

    var backLabel = ko.computed(function() {
      return self.editMode() ? 'Cancel': 'Back';
    });

    var endLabel = ko.computed(function() {
      return self.customerLocationMapVisible() ? '' : (self.editMode() ? 'Save': 'Edit');
    });

    // Setup header moduleConfig
    var headerViewModelParams = {
      title: headerTitle,
      startBtn: {
        id: 'backBtn',
        click: leftClickAction,
        display: 'icons',
        label: backLabel,
        icons: 'oj-hybrid-applayout-header-icon-back oj-fwk-icon',
        visible: true
      },
      endBtn: {
        id: 'nextBtn',
        click: rightClickAction,
        display: 'all',
        label: endLabel,
        icons: '',
        visible: true,
        disabled: app.isReadOnlyMode ? self.editMode : false
      }
    };

    moduleHelper.setupStaticModule(self, 'headerConfig', 'basicHeader', headerViewModelParams);

    // check if cordova contacts plugin is supported
    self.contactsPluginSupported = function() {
      return navigator.contacts !== undefined
    };

    // add custoemr to device contacts
    self.addToContacts = function() {
      var saveSuccess = function(contact) {
        app.enqueMessage({
          severity: 'info',
          summary: self.contactUpdateSummary(),
          detail: self.contactUpdateDetail(),
          autoTimeout: 0
        });
        self._openContact(contact.id);
      };

      var saveError = function(contactError) {
        oj.Logger.error('Failed to save to contacts.', contactError)
      };

      var createContact = function() {
        var contactToSave = navigator.contacts.create();
        var contact = ko.mapping.toJS(self.customerModel);
        contactToSave.displayName = contact.firstName + ' ' + contact.lastName;
        contactToSave.nickname = contact.firstName;

        var name = new ContactName();
        name.givenName = contact.firstName;
        name.familyName = contact.lastName;
        name.formatted = contactToSave.displayName;
        contactToSave.name = name;

        var phoneNumbers = [];
        if (contact.mobile)
          phoneNumbers[0] = new ContactField('mobile', contact.mobile, false);
        if (contact.home)
          phoneNumbers[1] = new ContactField('home', contact.home, false);
        contactToSave.phoneNumbers = phoneNumbers;

        var emails = [];
        if (contact.email)
          emails[0] = new ContactField('work', contact.email);
        contactToSave.emails = emails;

        var addresses = [];
        if (contact.address) {
          addresses[0] = new ContactAddress();
          addresses[0].type = 'work';
          addresses[0].formattedAddress = contact.address.formatted;
          addresses[0].streetAddress = (contact.address.street1 + ' ' + contact.address.street2).trim();
          addresses[0].locality = contact.address.city;
          addresses[0].region = contact.address.state;
          addresses[0].postalCode = contact.address.zip;
          addresses[0].country = contact.address.country;
          contactToSave.addresses = addresses;
        }

        contactToSave.save(saveSuccess, saveError);
      }

      var onSuccess = function(contacts) {
        if (contacts.length > 0) {
          self.contactUpdateSummary('Contact Updated');
          self.contactUpdateDetail('The customer was successfully updated to your contacts');
          contacts[0].remove(createContact, saveError);
        } else {
          self.contactUpdateSummary('Contact Created');
          self.contactUpdateDetail('The customer was successfully added to your contacts');
          createContact();
        }
      };

      var onError = function(contactError) {
        oj.Logger.error('Failed to find contacts.', contactError);
      };

      // look for existing contacts
      var options = new ContactFindOptions();
      options.filter = self.customerModel().firstName() + ' ' + self.customerModel().lastName();
      options.multiple = true;
      options.desiredFields = [navigator.contacts.fieldType.id];
      options.hasPhoneNumber = true;
      var fields = [navigator.contacts.fieldType.displayName, navigator.contacts.fieldType.name];
      navigator.contacts.find(fields, onSuccess, onError, options);
    };

    self._openContact = function(id) {
      var successCallback = function() {
        oj.Logger.info('multiwindow success');
      };

      var errorCallback = function(msg) {
        oj.Logger.error(msg);
      };

      if (window.samsung && window.samsung.multiwindow) {
        window.samsung.multiwindow.isSupported("freestyle", function() {
          var inputOptions = {};
          inputOptions.windowType = 'freestyle';
          inputOptions.action = "action_view";
          inputOptions.scaleInfo = 80;
          inputOptions.dataUri = "content://contacts/people/" + id;
          window.samsung.multiwindow.createMultiWindow(inputOptions, successCallback, errorCallback);
        }, function(){
          oj.Logger.error('no Samsung Multiwindow plugin');
        });
      }
    };

    self.showCustomerLocationMap = function() {
      self.customerLocationMapVisible(true);
    };
  }

  return customerDetails;
});
