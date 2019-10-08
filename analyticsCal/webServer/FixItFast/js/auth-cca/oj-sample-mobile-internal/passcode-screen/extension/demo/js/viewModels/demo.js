/**
 * @license
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
define(['knockout', 'ojs/ojknockout', 'ojs/ojbutton', 'ojs/ojformlayout', 'ojs/ojinputtext', 'ojs/ojinputnumber', 'ojs/ojswitch',
        'oj-sample-mobile-internal/passcode-screen/loader'],
  function(ko) {
    function PasscodeModel(params) {
      var self = this;
      // For oj-sample demo
      self.addNav = ko.observable(false);
      if (params && params.menuSignal) {
        self.menuSignal = params.menuSignal;
        self.addNav(true);
      }

      self.goBack = function(event) {
        return self.menuSignal && self.menuSignal.dispatch('componentMenu');
      };
      // End: For oj-sample demo

      self.passcode = ko.observable();
      self.companyName = ko.observable('myCompany');
      self.appName = ko.observable('myApp');
      self.passcodeTxt = ko.observable('Provide passcode');
      self.goText = ko.observable('Go!');
      self.delText = ko.observable('<-');
      self.validateLen = ko.observable(true);
      self.minLen = ko.observable(4);
      self.maxLen = ko.observable(8);
      self.done = function() {
        self.passcode(document.getElementById("passcodeScreen").getPasscode());
      };

      self.clear = function() {
        document.getElementById("passcodeScreen").clearPasscode();
        self.done();
      }

      self.customError = function() {
        document.getElementById("passcodeScreen").setError('This is a custom error message!');
      }
    }

    return PasscodeModel;
  }
);