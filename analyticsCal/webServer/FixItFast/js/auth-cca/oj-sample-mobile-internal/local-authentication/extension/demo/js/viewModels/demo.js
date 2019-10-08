/**
 * @license
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
define(['ojs/ojcontext', 'knockout',
        'oj-sample-mobile-internal/common/auth-error-translations',
        'ojs/ojknockout', 'ojs/ojbutton', 'ojs/ojswitch', 'ojs/ojformlayout',
        'oj-sample-mobile-internal/local-authentication/loader', 'ojs/ojmessages'],
  function(Context, ko, errTsl) {
    var LocalAuthModel = function(params) {
      this.configureBtnDisabled = ko.observable(false);

      // For oj-sample demo
      this.addNav = ko.observable(false);
      if (params && params.menuSignal) {
        this.menuSignal = params.menuSignal;
        this.addNav(true);
      }

      // End: For oj-sample demo

      this.plugin = window.cordova && window.cordova.plugins && window.cordova.plugins.IdmAuthFlows;
      this.enableResume = ko.observable(true);
      this.showDismiss = ko.observable(true);
      this.messages = ko.observableArray();
      this.messagePos = ko.observable({
        'my': {'vertical' :'top', 'horizontal': 'end'},
        'at': {'vertical': 'top', 'horizontal': 'end'},
        'of': 'window'
      });
  
      if (this.plugin)
        this.localAuthBuilder = new cordova.plugins.IdmAuthFlows.LocalAuthPropertiesBuilder().id("LocalAuthDemo");
    };

    // Lifecycle methods
    LocalAuthModel.prototype.connected = function() {
      // If there is any authenticator enabled, user can configure
      // only after authenticating.
      if (!this.plugin) 
        return;
      var cca = document.getElementById("localAuth");

      Context.getContext(cca).getBusyContext().whenReady()
      .then(function(){
        return cca.getFlowPromise();
      }) 
      .then(function(flow) {
        return flow.getManager().getEnabled();
      })
      .then(function(enabled) {
        this.configureBtnDisabled(enabled.length > 0);
      }.bind(this));
    };

    // Event listerners
    LocalAuthModel.prototype.login = function(event, vm) {
      document.getElementById("localAuth").getFlowPromise()
        .then(function(flow) {
          vm.localAuthFlow = flow;
          return flow.getManager().getEnabled();
        })
        .then(function(enabled) {
          if (enabled.length === 0)
            return Promise.resolve();

          return vm.localAuthFlow.login();
        })
        .then(function() {
          vm.configureBtnDisabled(false);
          vm.enqueMessage({
            autoTimeout: 0,
            severity: 'info', 
            summary: 'Authentication successful', 
            detail: 'Local authentication was successfully completed.'});
        })
        .catch(function(err) {
          vm.enqueMessage({
            autoTimeout: 0,
            severity: 'error', 
            summary: 'Authentication failed', 
            detail: 'Local authentication failed. Reason:' + errTsl.getTranslationForError(err)});
        });
    };

    LocalAuthModel.prototype.dismissConfig = function() {
      document.getElementById("localAuth").dismissConfigureScreen();
    };

    LocalAuthModel.prototype.configure = function(event, vm) {
      document.getElementById("localAuth").launchConfigureScreen();
      vm.enqueMessage({
        autoTimeout: 0,
        severity: 'info', 
        summary: 'Configuration', 
        detail: 'Config screen is launched successfully.'});
    };

    LocalAuthModel.prototype.dismissedConfig = function(event, vm) {
      vm.enqueMessage({
        autoTimeout: 0,
        severity: 'info', 
        summary: 'Configuration', 
        detail: 'Config screen is dismissed successfully.'});
    };   
    
    LocalAuthModel.prototype.enqueMessage = function(message) {
      this.messages.push(message);
    };

    LocalAuthModel.prototype.onMessage = function(event, vm) {
      vm.enqueMessage(event.detail.message);
    }

    LocalAuthModel.prototype.goBack = function(event, vm) {
      return vm.menuSignal && vm.menuSignal.dispatch('componentMenu');
    };

    LocalAuthModel.prototype.cancelMessage = function(event, vm) {
      vm.messages.remove(event.detail.message);
    };

    return LocalAuthModel;
  }
);
