/**
 * @license
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
/**
 * Copyright (c) 2015, 2018, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
'use strict';
define(
    ['ojs/ojtranslation', 'knockout',
     'ojL10n!./resources/nls/passcode-screen-strings',
     'ojs/ojbutton', 'ojs/ojinputtext'],
  function (Translations, ko, nls) {
    function PasscodeScreenModel(context) {
      this.context = context;
      this.composite = context.element;
      this.translations = nls.ojSampleMobilePasscodeScreen;
      this.initObservables();
    };

    PasscodeScreenModel.StringProperties = ['appName', 'companyName', 'passcodeText', 'goText', 'deleteText'];

    /**
     * Method to init observables needed by component.
     * @internal
     */
    PasscodeScreenModel.prototype.initObservables = function() {
      this.passcode = ko.observable('');
      this.errorMsg = ko.observable();
      this.initComponentProperties();
    };

    /**
     * Method to init component properties.
     * @internal
     */
    PasscodeScreenModel.prototype.initComponentProperties = function() {
      PasscodeScreenModel.StringProperties.forEach(function(el) {
        this.initStringProperty(el);
      }.bind(this));

      this.validatePasscodeLength = ko.observable(false);
      this.minLen = ko.observable(4);
      this.maxLen = ko.observable(12);

      if (this.context.properties.minPasscodeLength)
        this.minLen(this.context.properties.minPasscodeLength);
      if (this.context.properties.maxPasscodeLength)
        this.maxLen(this.context.properties.maxPasscodeLength);
      if (this.context.properties.validatePasscodeLength)
        this.validatePasscodeLength(true);
    };

    /**
     * Handle property changes done from app.
     * @param {object} context 
     */
    PasscodeScreenModel.prototype.propertyChanged = function(context) {
      for (var index in PasscodeScreenModel.StringProperties)
        if (this.handleStringChanged(context, PasscodeScreenModel.StringProperties[index]))
          return;

      if (context.property === 'validatePasscodeLength' && context.value !== this.validatePasscodeLength()) {
        this.validatePasscodeLength(context.value);
        return;
      }

      if (context.property === 'minPasscodeLength' && context.value !== this.minLen()) {
        this.minLen(context.value);
        return;
      } 
      
      if (context.property === 'maxPasscodeLength' && context.value !== this.maxLen())
        this.maxLen(context.value);
    };

    /**
     * Handle component configured property changed for string types.
     * @param {object} context 
     * @param {string} key 
     */
    PasscodeScreenModel.prototype.handleStringChanged = function(context, key) {
      if (context.property !== key || context.value === this[key]()) 
        return false;

      if (context.value === undefined)
        this[key](this.defaultString(key));
      else 
        this[key](context.value);

      return true;
    };

    /**
     * Method to fetch and set display string passed in component properties
     * and default to translated strings if missing.
     * @param {String} key 
     * @internal
     */
    PasscodeScreenModel.prototype.initStringProperty = function(key) {
      var displayStr;
      if (this.context.properties[key])
        displayStr = this.context.properties[key];
      else
        displayStr = this.defaultString(key);
      this[key] = ko.observable(displayStr);
    };

    /**
     * Returns default string from translations for a key provided.
     * @param {string} key 
     */
    PasscodeScreenModel.prototype.defaultString = function(key) {
      return this.translations['default' + key.charAt(0).toUpperCase() + key.slice(1)];
    };

    // UI event handlers.
    /**
     * Handler for keypad buttons 
     * @param {object} event 
     * @param {object} vm 
     * @internal
     */
    PasscodeScreenModel.prototype.keypadButtonClick = function(event, vm) {
      // Note: event.srcElement.innerText will change with translation.
      vm.passcode(vm.passcode() + event.srcElement.innerText);
    };

    /**
     * Handler for delete button on keypad
     * @param {object} event 
     * @param {object} vm 
     * @internal
     */
    PasscodeScreenModel.prototype.deleteChar = function(event, vm) {
      vm.passcode(vm.passcode().slice(0, -1));
    };

    /**
     * Handler for submit button on the keypad
     * @param {object} event 
     * @param {object} vm 
     * @internal
     */
    PasscodeScreenModel.prototype.submitPin = function(event, vm) {
      var passLen = vm.passcode().length;
      if (vm.validatePasscodeLength() && (passLen < vm.minLen() || passLen > vm.maxLen())) {
        vm.errorMsg(Translations.applyParameters(vm.translations.lengthValidationError, [vm.minLen(), vm.maxLen()]));
        return;
      }

      vm.errorMsg('');
      vm.composite.dispatchEvent(new CustomEvent('ojDone', {bubbles: true, details: {}}));
    };

    // Public methods.
    /**
     * Public method to get passcode entered by user.
     */
    PasscodeScreenModel.prototype.getPasscode = function() {
      return this.passcode();
    };

    /**
     * Public method to clear passcode.
     */
    PasscodeScreenModel.prototype.clearPasscode = function() {
      this.passcode('');
    };

    /**
     * Public method to set error message on the keypad.
     */
    PasscodeScreenModel.prototype.setError = function(error) {
      this.errorMsg(error);
    };

    return PasscodeScreenModel;
});