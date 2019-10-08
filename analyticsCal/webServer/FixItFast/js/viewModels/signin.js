/**
 * @license
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
/**
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */

 // signin page viewModel
 // In a real app, replace it with your authentication and logic
'use strict';
define(['ojs/ojcore', 'knockout', 'appController', 'appUtils',
        'ojs/ojknockout',
        'ojs/ojcheckboxset',
        'ojs/ojinputtext',
        'ojs/ojbutton',
        'ojs/ojvalidationgroup',
        'ojs/ojanimation'], function(oj, ko, app, appUtils) {
  function signin() {
    var self = this;

    self.transitionCompleted = function() {
      appUtils.setFocusAfterModuleLoad('signInBtn');
      var animateOptions = { 'delay': 0, 'duration': '1s', 'timingFunction': 'ease-out' };
      oj.AnimationUtils['fadeIn'](document.getElementsByClassName('demo-signin-bg')[0], animateOptions);
    }

    self.groupValid = ko.observable();
    self.userName = ko.observable();
    self.passWord = ko.observable();
    self.rememberUserName = ko.observable();

    // First time, rememberUserName in sessionStorage will not be set. In this case we default to true.
    if (window.sessionStorage.rememberUserName === undefined || window.sessionStorage.rememberUserName === 'true') {
      app.getUserProfile()
        .then(function(userProfile) {
          self.userName(userProfile.firstName() + ' ' + userProfile.lastName());
        }).catch(function() {
          // This won't happen in general, because then that means the entire offline data loading is broken.
          // Use default user name if at all this happens.
          self.userName("Harry Calson");
        });
      self.passWord('password');
      self.rememberUserName(['remember']);
    }

    // Replace with sign in authentication
    self.signIn = function() {
      if (self.groupValid() !== "valid")
        return;

      window.sessionStorage.rememberUserName = '' + (self.rememberUserName() && self.rememberUserName().indexOf('remember') != -1);
      app.onLoginSuccess();
    };

  }
  return signin;
});
