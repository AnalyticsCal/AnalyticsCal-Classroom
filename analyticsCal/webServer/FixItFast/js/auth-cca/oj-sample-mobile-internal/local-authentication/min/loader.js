/**
 * @license
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */

define('text!oj-sample-mobile-internal/local-authentication/local-authentication-view.html',[],function () { return '<!--\n  Copyright (c) 2015, 2018, Oracle and/or its affiliates.\n  The Universal Permissive License (UPL), Version 1.0\n-->\n<div :id="[[\'page_\' + uniqueId]]" class="oj-hybrid-applayout-page">\n  <oj-bind-if test=\'[[isShowingConfigScreen]]\'>\n    <div :id="[[\'header_\' + uniqueId]]" class="oj-applayout-fixed-top">\n      <oj-bind-slot name="configHeader">\n      </oj-bind-slot>\n    </div>\n  </oj-bind-if>\n  <div :id="[[\'content_\' + uniqueId]]" class="oj-applayout-content oj-complete">\n    <oj-module :id="[[\'module_\' + uniqueId]]" config="[[moduleConfig]]"/>\n  </div>\n</div>\n';});

/**
  Copyright (c) 2015, 2018, Oracle and/or its affiliates.
  The Universal Permissive License (UPL), Version 1.0
*/
define('oj-sample-mobile-internal/local-authentication/resources/nls/local-authentication-strings',{
  "root": true
});

/**
  Copyright (c) 2015, 2018, Oracle and/or its affiliates.
  The Universal Permissive License (UPL), Version 1.0
*/
define('oj-sample-mobile-internal/common/resources/nls/auth-error-translations-strings',{
  "root": true
});


/**
  Copyright (c) 2015, 2018, Oracle and/or its affiliates.
  The Universal Permissive License (UPL), Version 1.0
*/

define('oj-sample-mobile-internal/common/auth-error-translations',['ojL10n!./resources/nls/auth-error-translations-strings'],
  function (translations) {
    function ErrorTranslationsModel() {
      this.translations = translations;
    }

    /**
     * Method to convert error object to translated error message.
     * @param {object} error 
     */
    ErrorTranslationsModel.prototype.getTranslationForError = function(error) {
      if (error.errorSource === 'system')
        return error.translatedErrorMessage;

      var message = this.translations.errorMessages[error.errorCode];
      if (!message)
        return this.translations.errorMessages.unknownErrorCode + error.errorCode;
      return message;
    };

    return new ErrorTranslationsModel();
  }
);
/**
  Copyright (c) 2015, 2018, Oracle and/or its affiliates.
  The Universal Permissive License (UPL), Version 1.0
*/

define(
    'oj-sample-mobile-internal/local-authentication/local-authentication-viewModel',['knockout',
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


define('text!oj-sample-mobile-internal/local-authentication/component.json',[],function () { return '{\n  "name": "local-authentication",\n  "pack":"oj-sample-mobile-internal",\n  "displayName": "Local authenticator",\n  "description": "Component to implement local authentication on mobile devices using IDM plugin.",\n  "version": "0.0.5",\n  "jetVersion": "^6.0.0",\n  "license": "https://opensource.org/licenses/UPL",\n  "dependencies": {\n    "oj-sample-mobile-internal-common":"0.0.4",\n    "oj-sample-mobile-internal-passcode-screen":"0.0.5",\n    "oj-ref-cordova-plugin-oracle-idm-auth": "^1.1.1"\n  },\n  "properties": {\n    "builder": {\n      "description": "Builder for local auth.",\n      "type": "object",\n      "required": true\n    },\n    "showDismissButton": {\n      "description": "If the done button to dismiss the configure screen should be shown or not. Defaults to false.",\n      "type": "boolean"\n    },\n    "enableResumeChallenge": {\n      "description": "If enabled, user will be challenged when app is restored to foreground from background. Defaults to false.",\n      "type": "boolean"\n    },\n    "maxPasscodeLength": {\n      "description": "Maximum length of passcode allowed, defaults to 4. This property is passed on to oj-sample-mobile-passcode-screen component that is internally used.",\n      "type": "number"\n    },\n    "minPasscodeLength": {\n      "description": "Minimum length of passcode allowed, defaults to 12. This property is passed on to oj-sample-mobile-passcode-screen component that is internally used.",\n      "type": "number"\n    },\n    "appName": {\n      "description": "Name of the app to be displayed on the passcode page. Has default value if not configured. This property is passed on to oj-sample-mobile-passcode-screen component that is internally used.",\n      "type": "string"\n    },\n    "companyName": {\n      "description": "Name of the company to be displayed on the passcode page. Has default value if not configured. This property is passed on to oj-sample-mobile-passcode-screen component that is internally used.",\n      "type": "string"\n    }\n  },\n  "methods": {\n    "getFlowPromise": {\n      "description": "Returns a promise which provides the authentication flow when it resolves."\n    },\n    "launchConfigureScreen": {\n      "description": "Display the configure screen."\n    },\n    "dismissConfigureScreen": {\n      "description": "Dismiss the configure screen. Can be used for dismissing programmatically when showDismissButton is set to false."\n    }\n  },\n  "events": {\n    "ojDismissed": {\n      "description": "Fired when the configuration screen is dismissed. This can be used to restore app content once use has exited the config screen.",\n      "bubbles": true\n    },\n    "ojResumeStart": {\n      "description": "Fired when onResume login is triggered.",\n      "bubbles": true\n    },\n    "ojResumeEnd": {\n      "description": "Fired when onResume login ends.",\n      "bubbles": true,\n      "detail": {\n        "success": {\n          "description": "If authentication was successful or not.",\n          "type": "boolean"\n        }\n      }\n    },\n    "ojMessage": {\n      "description": "Fires when there is a message to be displayed to the user.",\n      "bubbles": true,\n      "detail": {\n        "message": {\n          "description": "Object that contains details of the message. This can be used directly with oj-messages.",\n          "type": "object"\n        }\n      }\n    }\n  },\n  "slots": {\n    "configHeader": {\n      "description": "Slot for header section of configure screen."\n    }\n  },\n  "extension": {\n    "catalog": {\n      "category": "Mobile Components",\n      "tags": [\n        "IDM",\n        "authentication",\n        "mobile",\n        "Form Factor: Tablet",\n        "Form Factor: mobile"\n      ]\n    }\n  }\n}\n';});


define('css!oj-sample-mobile-internal/local-authentication/local-authentication-styles',[],function(){});

define('text!oj-sample-mobile-internal/passcode-screen/passcode-screen-view.html',[],function () { return '<!--\n  Copyright (c) 2015, 2018, Oracle and/or its affiliates.\n  The Universal Permissive License (UPL), Version 1.0\n-->\n<div class="dpls">\n  <div class="dpls-container">\n    <div>\n      <h1 class="dpls-appname dpls-white-text"><oj-bind-text value="[[companyName]]"></oj-bind-text>\n        <div><oj-bind-text value="[[appName]]"></oj-bind-text></div>\n      </h1>\n    </div>\n\n    <div class="dpls-passcode-area">\n      <div>\n        <h3 class="dpls-white-text"><oj-bind-text value="[[passcodeText]]"></oj-bind-text></h3>\n        <h4 class="dpls-red-text"><oj-bind-text value="[[errorMsg]]"></oj-bind-text></h4>\n      </div>\n      <div class="dpls-passcode-input-area">\n        <div class="dpls-passcode-input-element">\n          <oj-input-password :id="[[\'pwdFld_\' + $uniqueId]]" value=\'{{passcode}}\' readonly></oj-input-password>\n        </div>\n        <div>\n          <oj-button class="dpls-white-text" chroming="half" on-click=\'[[submitPin]]\'>\n            <span><oj-bind-text value="[[goText]]"></oj-bind-text></span>\n          </oj-button>\n        </div>\n      </div>\n    </div>\n\n    <div class="dpls-keypad dpls-white-text">\n      <div class="dpls-keypad-row">\n        <div class="dpls-round-btn" on-click=\'[[keypadButtonClick]]\'>\n          <oj-bind-text value="[[translations.one]]"></oj-bind-text>\n        </div>\n        <div class="dpls-round-btn" on-click=\'[[keypadButtonClick]]\'>\n          <oj-bind-text value="[[translations.two]]"></oj-bind-text>\n        </div>\n        <div class="dpls-round-btn" on-click=\'[[keypadButtonClick]]\'>\n          <oj-bind-text value="[[translations.three]]"></oj-bind-text>\n        </div>\n      </div>\n      <div class="dpls-keypad-row">\n        <div class="dpls-round-btn" on-click=\'[[keypadButtonClick]]\'>\n          <oj-bind-text value="[[translations.four]]"></oj-bind-text>\n        </div>\n        <div class="dpls-round-btn" on-click=\'[[keypadButtonClick]]\'>\n          <oj-bind-text value="[[translations.five]]"></oj-bind-text>\n        </div>\n        <div class="dpls-round-btn" on-click=\'[[keypadButtonClick]]\'>\n          <oj-bind-text value="[[translations.six]]"></oj-bind-text>\n        </div>\n      </div>\n      <div class="dpls-keypad-row">\n        <div class="dpls-round-btn" on-click=\'[[keypadButtonClick]]\'>\n          <oj-bind-text value="[[translations.seven]]"></oj-bind-text>\n        </div>\n        <div class="dpls-round-btn" on-click=\'[[keypadButtonClick]]\'>\n          <oj-bind-text value="[[translations.eight]]"></oj-bind-text>\n        </div>\n        <div class="dpls-round-btn" on-click=\'[[keypadButtonClick]]\'>\n          <oj-bind-text value="[[translations.nine]]"></oj-bind-text>\n        </div>\n      </div>\n      <div class="dpls-keypad-row">\n        <div class="dpls-dummy-btn"></div>\n        <div class="dpls-round-btn" on-click=\'[[keypadButtonClick]]\'>\n          <oj-bind-text value="[[translations.zero]]"></oj-bind-text>\n        </div>\n        <div class="dpls-delete-btn-container">\n          <oj-button class="dpls-white-btn" chroming="half" on-click=\'[[deleteChar]]\'>\n            <span><oj-bind-text value="[[deleteText]]"></oj-bind-text></span>\n          </oj-button>\n        </div>\n      </div>\n    </div>\n  </div>\n</div>\n';});

/**
  Copyright (c) 2015, 2018, Oracle and/or its affiliates.
  The Universal Permissive License (UPL), Version 1.0
*/
define('oj-sample-mobile-internal/passcode-screen/resources/nls/passcode-screen-strings',{
  "root": true
});


/**
 * Copyright (c) 2015, 2018, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */

define(
    'oj-sample-mobile-internal/passcode-screen/passcode-screen-viewModel',['ojs/ojtranslation', 'knockout',
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

define('text!oj-sample-mobile-internal/passcode-screen/component.json',[],function () { return '{\n  "name": "passcode-screen",\n  "pack":"oj-sample-mobile-internal",\n  "displayName": "Passcode based login screen",\n  "description": "Login screen for collecting passcode from user.",\n  "version": "0.0.5",\n  "jetVersion": "^6.0.0",\n  "properties": {\n    "appName": {\n      "description": "Name of the app to be displayed on the login page. Has default value if not configured.",\n      "type": "string"\n    },\n    "companyName": {\n      "description": "Name of the company to be displayed on the login page. Has default value if not configured.",\n      "type": "string"\n    },\n    "passcodeText": {\n      "description": "Text to be used for passcode prompt. Has default value if not configured.",\n      "type": "string"\n    },\n    "goText": {\n      "description": "Text to be used for submit button. Has default value if not configured.",\n      "type": "string"\n    },\n    "deleteText": {\n      "description": "Text to be used for delete button. Has default value if not configured.",\n      "type": "string"\n    },\n    "validatePasscodeLength": {\n      "description": "If passcode length validation should be triggered or not. Defaults to false.",\n      "type": "boolean"\n    },\n    "maxPasscodeLength": {\n      "description": "Maximum length of passcode allowed, defaults to 4.",\n      "type": "number"\n    },\n    "minPasscodeLength": {\n      "description": "Minimum length of passcode allowed, defaults to 12.",\n      "type": "number"\n    }\n  },\n  "methods": {\n    "getPasscode": {\n      "description": "Returns the passcode captured from user."\n    },\n    "clearPasscode": {\n      "description": "Clears the passcode currently held."\n    },\n    "setError": {\n      "description": "Sets error message to be shown to the user.",\n      "params" : [\n        {\n          "description":"Error message to use.",\n          "name" : "error",\n          "type": "string"\n        }\n      ]\n    }\n  },\n  "events": {\n    "ojDone": {\n      "description": "Fired when user clicks on go button to submit the passcode.",\n      "bubbles": true\n    }\n  },\n  "extension": {\n    "catalog": {\n      "category": "Mobile Components",\n      "tags": [\n        "IDM",\n        "authentication",\n        "mobile",\n        "Form Factor: Tablet",\n        "Form Factor: mobile"\n      ]\n    }\n  }\n}';});


define('css!oj-sample-mobile-internal/passcode-screen/passcode-screen-styles',[],function(){});
/**
  Copyright (c) 2015, 2018, Oracle and/or its affiliates.
  The Universal Permissive License (UPL), Version 1.0
*/
define('oj-sample-mobile-internal/passcode-screen/loader',['ojs/ojcomposite', 'text!./passcode-screen-view.html',
        './passcode-screen-viewModel', 'text!./component.json',
        'css!./passcode-screen-styles'],
  function(Composite, view, viewModel, metadata) {
    Composite.register('oj-sample-mobile-internal-passcode-screen', {
      view: view, 
      viewModel: viewModel, 
      metadata: JSON.parse(metadata)
    });
  }
);
/**
  Copyright (c) 2015, 2018, Oracle and/or its affiliates.
  The Universal Permissive License (UPL), Version 1.0
*/
define('oj-sample-mobile-internal/local-authentication/loader',['ojs/ojcomposite', 'text!./local-authentication-view.html',
        './local-authentication-viewModel', 'text!./component.json',
        'css!./local-authentication-styles', 
        'oj-sample-mobile-internal/passcode-screen/loader'],
  function(Composite, view, viewModel, metadata) {
    Composite.register('oj-sample-mobile-internal-local-authentication', {
      view: view, 
      viewModel: viewModel, 
      metadata: JSON.parse(metadata)
    });
  }
);

(function(c){var d=document,a='appendChild',i='styleSheet',s=d.createElement('style');s.type='text/css';d.getElementsByTagName('head')[0][a](s);s[i]?s[i].cssText=c:s[a](d.createTextNode(c));})
('oj-sample-mobile-local-authentication .dla-config-screen {\n  padding:10px;\n}oj-sample-mobile-internal-passcode-screen * {\n  box-sizing: border-box;\n}\n\noj-sample-mobile-internal-passcode-screen .dpls {\n  background-color:#3C72CE;\n  width: 100%;\n  min-height: 100vh;\n  display: flex;\n  flex-wrap: wrap;\n  justify-content: center;\n  align-items: center;\n}\n\noj-sample-mobile-internal-passcode-screen .dpls-container {\n  width:390px; /* Fix the width for the center passcode content */\n  display: flex;\n  flex-direction: column;\n}\n\noj-sample-mobile-internal-passcode-screen .dpls-appname {\n  font-size: 3rem;\n  text-align:center;\n}\n\noj-sample-mobile-internal-passcode-screen .dpls-appname > div {\n  font-weight: 400;\n  padding-top: 4px;\n\n}\n\noj-sample-mobile-internal-passcode-screen .dpls-passcode-area {\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  flex-direction: column;\n  text-align: center;\n}\n\noj-sample-mobile-internal-passcode-screen .dpls-passcode-input-area {\n  display: flex;\n  flex-direction: row;\n  align-items: center;\n  width: 100%;\n}\n\noj-sample-mobile-internal-passcode-screen .dpls-passcode-input-element {\n  width: 75%;\n  display: flex;\n  justify-content: flex-end;\n}\n\noj-sample-mobile-internal-passcode-screen .dpls-passcode-input-element .oj-inputpassword.oj-read-only .oj-inputpassword-input {\n  letter-spacing: 20px;\n  color: white;\n  font-size: 1.5rem;\n  text-align:center;\n}\n\noj-sample-mobile-internal-passcode-screen .dpls-keypad {\n  display: flex;\n  flex-wrap: wrap;\n  justify-content: center;\n}\n\noj-sample-mobile-internal-passcode-screen .dpls-keypad-row {\n  display: flex;\n  justify-content: space-around;\n  flex-wrap: nowrap;\n  width: 100%;\n  margin: 10px;\n}\n\noj-sample-mobile-internal-passcode-screen .dpls-dummy-btn {\n  height: 80px;\n  width: 70px; /* Find out why this has to be 10 px less */\n}\n\noj-sample-mobile-internal-passcode-screen .dpls-round-btn {\n  border: solid 1px;\n  border-color: #82B9E7;\n  border-radius: 50%;\n  font-size: 2.5rem;\n  cursor:default;\n  height: 80px;\n  width: 80px;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n}\n\noj-sample-mobile-internal-passcode-screen .dpls-round-btn:hover {\n  background-color:#76b8e1;\n  border-color: white;\n}\n\noj-sample-mobile-internal-passcode-screen .dpls-delete-btn-container {\n  display: flex;\n  align-items: center;\n  justify-content: center;\n}\n\noj-sample-mobile-internal-passcode-screen .dpls-white-text {\n  color:white;\n}\n\noj-sample-mobile-internal-passcode-screen .dpls-red-text {\n  color:#cc0000;\n}\n\noj-sample-mobile-internal-passcode-screen .dpls-white-text .oj-button-button > .oj-button-label > .oj-button-text {\n  color:white;\n}\n\n\n');

//# sourceMappingURL=loader.js.map