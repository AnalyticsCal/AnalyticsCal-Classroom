/**
 * @license
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
/**
 * Module for setting up a new passcode for the user.
 * This module captures passcode from the user when PIN authentication is enabled first time or user changes the passcode.
 */
define(['ojs/ojanimation', 'knockout',
        'ojs/ojknockout', 'ojs/ojinputtext',
        'ojs/ojbutton'],
  function(AnimationUtils, ko) {
    var pinChallengeReason = cordova.plugins.IdmAuthFlows.LocalAuthPropertiesBuilder.PinChallengeReason;
    var PasscodeChallengeModel = function(params) {
      var self = this;
      self.challengeReason = params.challengeReason;
      self.completionHandler = params.completionHandler;
      self.parentVM = params.parentVM;
      self.translations = self.parentVM.translations.ojSampleMobileLocalAuthentication.passcodeChallenge;
      self.appName = self.parentVM.appName;
      self.companyName = self.parentVM.companyName;
      self.minLen = self.parentVM.minLen;
      self.maxLen = self.parentVM.maxLen;
      self.context = self.parentVM.context;
      self.uniqueId = self.context.uniqueId;
      self.changePasscodeFlow = ko.observable(false);
      self.newPasscodeFlow = ko.observable(false);
      self.loginFlow = ko.observable(false);

      if (self.challengeReason === pinChallengeReason.Login)
        self.loginFlow(true);
      else if (self.challengeReason === pinChallengeReason.ChangePin)
        self.changePasscodeFlow(true);
      else if (self.challengeReason === pinChallengeReason.SetPin)
        self.newPasscodeFlow(true);
    };

    /**
     * Lifecycle method
     */
    PasscodeChallengeModel.prototype.transitionCompleted = function() {
      if (this.loginFlow() || this.changePasscodeFlow())
        this.show('captureCurrentPasscode');

      if (this.newPasscodeFlow())
        this.show('capturePasscode1');
    };

    /**
     * Find a DOM by ID + uniqueId
     * @param {string} id 
     * @internal
     */
    PasscodeChallengeModel.prototype.getById = function(id) {
      return document.getElementById(id + '_' + this.uniqueId);
    };

    /**
     * Hide a DOM element
     * @param {string} id
     * @internal 
     */
    PasscodeChallengeModel.prototype.hide = function(id) {
      return this.getById(id).setAttribute('style', 'display:none;');
    };

    /**
     * Show a DOM element
     * @param {string} id 
     * @internal 
     */
    PasscodeChallengeModel.prototype.show = function(id) {
      return this.getById(id).setAttribute('style', 'display:block;');
    };

    // Event handlers
    /**
     * Handler triggered when current passcode is captured.
     * @param {object} event 
     * @param {object} vm 
     */
    PasscodeChallengeModel.prototype.currPasscodeCaptured = function(event, vm) {
      if (vm.challengeReason === pinChallengeReason.Login) {
        vm.completionHandler.submit(vm.getById('currPasscode').getPasscode());
        vm.parentVM.hide();
        return;
      }

      vm.hide('captureCurrentPasscode');
      vm.show('capturePasscode1');
      AnimationUtils.slideIn(vm.getById('capturePasscode1'));
    };

    /**
     * Handler triggered when new passcode1 is entered by the user.
     * @param {object} event 
     * @param {object} vm 
     */
    PasscodeChallengeModel.prototype.passcode1Captured = function(event, vm) {
      vm.hide('capturePasscode1');
      vm.show('capturePasscode2');
      AnimationUtils.slideIn(vm.getById('capturePasscode2'));
    };

    /**
     * Handler triggered when new passcode is re-entered by the user.
     * @param {object} event 
     * @param {object} vm 
     */
    PasscodeChallengeModel.prototype.passcode2Captured = function(event, vm) {
      var passcode1Cca = vm.getById('passcode1');
      var passcode2Cca = vm.getById('passcode2');
      var currPasscodeCca = vm.getById('currPasscode');

      if (passcode1Cca.getPasscode() !== passcode2Cca.getPasscode()) {
        vm.recapturePasscode(passcode1Cca, passcode2Cca);
        return;
      }

      vm.completionHandler.submit(currPasscodeCca.getPasscode(), passcode1Cca.getPasscode());
      vm.parentVM.hide();
    };

    /**
     * This method prompt for retry, when user provides non-matching passcodes.
     * @param {object} passcode1Cca 
     * @param {object} passcode2Cca 
     */
    PasscodeChallengeModel.prototype.recapturePasscode = function(passcode1Cca, passcode2Cca) {
      passcode1Cca.setError(this.translations.passcodeMismatch);
      passcode1Cca.clearPasscode();
      passcode2Cca.clearPasscode();
      this.hide('capturePasscode2');
      this.show('capturePasscode1');
      AnimationUtils.slideIn(this.getById('capturePasscode1'));
    };
  
    /**
     * This is not implmeneted as of now. Consider cancel button in next release.
     * @param {object} event 
     * @param {object} vm 
     */
    PasscodeChallengeModel.prototype.cancel = function(event, vm) {
      vm.completionHandler.cancel();
      vm.parentVM.hide();
    };

    return PasscodeChallengeModel;
  }
);
