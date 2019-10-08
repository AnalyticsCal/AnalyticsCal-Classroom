/**
 * @license
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
/**
  Copyright (c) 2015, 2018, Oracle and/or its affiliates.
  The Universal Permissive License (UPL), Version 1.0
*/
'use strict';
define(
    ['knockout',
      'ojL10n!./resources/nls/local-authentication-strings',
      'oj-sample-mobile-internal/common/auth-error-translations',
      'ojs/ojmodule-element-utils',
      'ojs/ojmodule'
      ],
  function (ko, translations, errTsl, moduleUtils) {
    function LocalAuthViewModel(context) {
      this.context = context;
      this.uniqueId = context.uniqueId;
      this.translations = translations;
      this.composite = context.element;
      this.initObservables();
      this.initAuthFlow();
    }

    // Internal methods
    /**
     * Method to init observables needed by component.
     * @internal
     */
    LocalAuthViewModel.prototype.initObservables = function() {
      this.isShowingConfigScreen = ko.observable(false);
      this.moduleConfig = ko.observable({view:[]});
      var ccaRoot = require.toUrl('oj-sample-mobile-internal');
      var appRoot = require.toUrl('.');
      this.ccaModulePath = ccaRoot.replace(appRoot, '');
      this.initComponentProperties();
    };

    /**
     * Method to init component properties.
     * @internal
     */
    LocalAuthViewModel.prototype.initComponentProperties = function() {
      this.showDismissButton = ko.observable(false);
      
      if (this.context.properties.showDismissButton)
        this.showDismissButton(true);

      this.enableResumeChallenge  = false;
      if (this.context.properties.enableResumeChallenge)
        this.enableResumeChallenge = true;

      this.appName = this.context.properties.appName;
      this.companyName = this.context.properties.companyName;
      
      this.minLen = this.context.properties.minPasscodeLength;
      this.maxLen = this.context.properties.maxPasscodeLength;
    };

    LocalAuthViewModel.prototype.propertyChanged = function(context) {
      if (context.property === 'appName' && context.value !== this.appName()) {
        this.appName(context.value);
        return;
      }
      if (context.property === 'companyName' && context.value !== this.companyName()) {
        this.companyName(context.value);
        return;
      }

      if (context.property === 'showDismissButton' && context.value !== this.showDismissButton()) {
        this.showDismissButton(context.value);
        return;
      }

      if (context.property === 'enableResumeChallenge' && context.value !== this.enableResumeChallenge) {
        this.enableResumeChallenge = context.value;
        this.setupOnResumeChallenge();
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
     * Method to init authentication flow.
     * @internal
     */
    LocalAuthViewModel.prototype.initAuthFlow = function() {
      var builder = this.context.properties.builder;
      builder.pinChallengeCallback(this.pinChallengeCallback.bind(this));
      builder.translations(this.translations.ojSampleMobileLocalAuthentication.fingerprint, false);
      this.initPromise = cordova.plugins.IdmAuthFlows.init(builder.build());
      this.initPromise
      .then(function(flow) {
        this.localAuthFlow = flow;
        this.setupOnResumeChallenge();
      }.bind(this))
      .catch(function(err) {
        this.fireMessageEvent('error', this.translations.ojSampleMobileLocalAuthentication.initError, errTsl.getTranslationForError(err));
      }.bind(this));
    };

    LocalAuthViewModel.prototype.show = function(visible) {
      document.getElementById('page_' + this.uniqueId).style.display = 'block';
    }

    /**
     * Challenge callback to handle PIN related challenge from plugin.
     * @param {object} challengeReason 
     * @param {object} completionHandler 
     * @internal
     */
    LocalAuthViewModel.prototype.pinChallengeCallback = function(challengeReason, completionHandler) {
      this.isShowingConfigScreen(false);

      var contentEl = document.getElementById('content_' + this.uniqueId);
      var contentTopPadding = contentEl.style.paddingTop;
      if (contentTopPadding && contentTopPadding !== '0px')
        this.contentPadding = contentEl.style.paddingTop;

      contentEl.style.paddingTop = '0px';

      var viewPath = this.ccaModulePath + '/local-authentication/modules/views/passcode-challenge-handler.html';
      var modelPath = this.ccaModulePath + '/local-authentication/modules/viewModels/passcode-challenge-handler';
      var moduleParams =  {
          completionHandler: completionHandler,
          challengeReason: challengeReason,
          parentVM: this
      };

      var masterPromise = Promise.all([
        moduleUtils.createView({'viewPath':viewPath}),
        moduleUtils.createViewModel({'viewModelPath':modelPath})
      ]);

      masterPromise.then(function(values) {
        var config = {};
        config.view = values[0];
        config.viewModel = new values[1](moduleParams);
        this.moduleConfig(config);
        this.show(true);
      }.bind(this));
    };

    /**
     * Method to authenticate
     * @internal
     */
    LocalAuthViewModel.prototype.authenticate = function() {
      var self = this;
      self.localAuthFlow.getManager().getEnabled()
        .then(function(enabled) {
          if (enabled.length === 0) 
            return;
          self.composite.dispatchEvent(new CustomEvent('ojResumeStart', {bubbles: true}));
          self.localAuthFlow.login()
          .then(function() {
            self.composite.dispatchEvent(new CustomEvent('ojResumeEnd', {bubbles: true, detail: {success: true}}));
          })
          .catch(function(err) {
            self.fireMessageEvent('error', self.translations.ojSampleMobileLocalAuthentication.authError, errTsl.getTranslationForError(err));
            self.composite.dispatchEvent(new CustomEvent('ojResumeEnd', {bubbles: true, detail: {success: false}}));
          });
        }.bind(this));
    };

    /**
     * Method to set up 'resume' handlers if needed as per component config.
     * @internal
     */
    LocalAuthViewModel.prototype.setupOnResumeChallenge = function() {
      if (!this.enableResumeChallenge) {
        if (this.resumeListener) {
          document.removeEventListener("resume", this.resumeListener, false);
          this.resumeListener = undefined;
        }
        return;
      }

      this.resumeListener = this.authenticate.bind(this);
      document.addEventListener("resume", this.resumeListener, false);
    };

    /**
     * Hides the component oj-module.
     * @internal
     */
    LocalAuthViewModel.prototype.hide = function() {
      document.getElementById('page_' + this.uniqueId).style.display = 'none';
      this.isShowingConfigScreen(false);
      this.moduleConfig({view: []});
    };

    /**
     * Enables / disables local authentication.
     * @internal
     */
    LocalAuthViewModel.prototype.modifyLocalAuth = function(authType, enable) {
      var promise;
      if (enable)
        promise = this.localAuthFlow.getManager().enable(authType);
      else 
        promise = this.localAuthFlow.getManager().disable(authType);
      
      var launchConfigureScreenCallback = this.launchConfigureScreen.bind(this);
      promise.then(launchConfigureScreenCallback)
        .catch(launchConfigureScreenCallback);

    };

    /**
     * Change passcode
     * @internal
     */
    LocalAuthViewModel.prototype.changePasscode = function() {
      var launchConfigureScreenCallback = this.launchConfigureScreen.bind(this);
      this.localAuthFlow.getManager().changePin()
        .then(launchConfigureScreenCallback)
        .catch(launchConfigureScreenCallback);
    };

    // Public methods
    /**
     * Method to return flow promise
     * @returns {Promise} promise to be used by app to obtain flow object
     */
    LocalAuthViewModel.prototype.getFlowPromise = function() {
      return this.initPromise;
    };

    /**
     * Method to launch config screen. This can be used by app to launch the config screen when needed.
     * @returns {Promise} promise to be used by app to obtain flow object
     */
    LocalAuthViewModel.prototype.launchConfigureScreen = function(err) {
      var self = this;
      if (err && typeof err === 'object')
        self.fireMessageEvent('error', this.translations.ojSampleMobileLocalAuthentication.configError, errTsl.getTranslationForError(err));

      if (self.contentPadding && self.contentPadding !== '0px') 
        document.getElementById('content_' + this.uniqueId).style.paddingTop = self.contentPadding;

      var viewPath = self.ccaModulePath + '/local-authentication/modules/views/configurator.html';
      var modelPath = self.ccaModulePath + '/local-authentication/modules/viewModels/configurator';

      var masterPromise = Promise.all([
        moduleUtils.createView({'viewPath':viewPath}),
        moduleUtils.createViewModel({'viewModelPath':modelPath}),
        cordova.plugins.IdmAuthFlows.LocalAuthenticationHelper.getLocalAuthSupportInfo(),
        self.localAuthFlow.getManager().getEnabled()
      ]);

      masterPromise.then(function(results) {
        var config = {};
        config.view = results[0];

        config.viewModel = new results[1]({
          parentVM: self,
          localAuthSupports: results[2],
          enabledAuths: results[3]
        });
        self.isShowingConfigScreen(true);
        self.moduleConfig(config);
        self.show();
      });
    };

    /**
     * Method to dismiss config screen. This can be used by app to dismiss the config screen when needed.
     */
    LocalAuthViewModel.prototype.dismissConfigureScreen = function() {
      this.composite.dispatchEvent(new CustomEvent('ojDismissed', {bubbles: true}));
      this.hide();
    };

    LocalAuthViewModel.prototype.fireMessageEvent = function(severity, summary, message) {
      var detail = {
        message: {
          severity: severity,
          summary: summary,
          detail: message,
          autoTimeout: 0
        }
      };
      this.composite.dispatchEvent(new CustomEvent('ojMessage', {bubbles: true, detail: detail}));
    };

    return LocalAuthViewModel;
});
