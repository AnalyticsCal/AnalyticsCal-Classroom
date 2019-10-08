/**
 * @license
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
/**
 * Module for configuring local authentication settings.
 * self.module can be used for enabling / disabling Passcode or fingerprint and to change Passcode.
 */
define(['knockout', 'ojs/ojknockout', 'ojs/ojswitch', 'ojs/ojlabel', 'ojs/ojbutton'],
  function(ko) {
    var localAuthType = cordova.plugins.IdmAuthFlows.LocalAuthPropertiesBuilder.LocalAuthenticatorType;
    var localAuthAvailability = cordova.plugins.IdmAuthFlows.LocalAuthenticationHelper.Availability;
    var ConfigureModel = function(params) {
      this.parentVM = params.parentVM;
      this.translations = this.parentVM.translations.ojSampleMobileLocalAuthentication.configure;
      this.showDismissButton = this.parentVM.showDismissButton;
      this.context = this.parentVM.context;
  
      this.fingerprintNotAllowed = ko.observable(true);
      var message;
      switch(params.localAuthSupports[localAuthType.Fingerprint]) {
        case localAuthAvailability.Enrolled:
          this.fingerprintNotAllowed(false);
          break;
        case localAuthAvailability.NotEnrolled:
          message = this.translations.fingerprintAvailableNotEnrolled;
          break;
        case localAuthAvailability.LockedOut:
          message = this.translations.fingerprintLocked;
          break;
        case localAuthAvailability.NotAvailable:
          message = this.translations.fingerprintUnavailable;
          break;
      }

      if (message)
       this.parentVM.fireMessageEvent('warning', this.translations.fingerprintMessageHeader, message);
      var enabledAuths = params.enabledAuths;
      this.passcodeEnabled = ko.observable(enabledAuths.indexOf(localAuthType.PIN) > -1);
      this.fingerprintEnabled = ko.observable(enabledAuths.indexOf(localAuthType.Fingerprint) > -1);
    };

    /**
     * Handler for swich option change for enabling / disabling passcode or fingerprint.
     * @param {object} event 
     * @param {object} vm 
     */
    ConfigureModel.prototype.optionChanged = function(event, vm) {
      var authType;
      var eventId = event.srcElement.id;
      var uniqueId =  vm.context.uniqueId;

      if (eventId == 'togglePasscode_' + uniqueId) {
        authType = localAuthType.PIN;
      } else if (eventId == 'toggleFingerprint_' + uniqueId) {
        authType = localAuthType.Fingerprint;
      }

      vm.parentVM.modifyLocalAuth(authType, event.detail.value);
    };

    /**
     * Handler for change passcode button.
     * @param {object} event 
     * @param {object} vm 
     */
    ConfigureModel.prototype.changePasscode = function(event, vm) {
      vm.parentVM.changePasscode();
    };

    /**
     * Dismisses configuration screen
     * @param {object} event 
     * @param {object} vm 
     */
    ConfigureModel.prototype.dismiss = function(event, vm) {
      vm.parentVM.dismissConfigureScreen();
    };

    return ConfigureModel;
  }
);
