/**
 * @license
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */

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

(function(c){var d=document,a='appendChild',i='styleSheet',s=d.createElement('style');s.type='text/css';d.getElementsByTagName('head')[0][a](s);s[i]?s[i].cssText=c:s[a](d.createTextNode(c));})
('oj-sample-mobile-internal-passcode-screen * {\n  box-sizing: border-box;\n}\n\noj-sample-mobile-internal-passcode-screen .dpls {\n  background-color:#3C72CE;\n  width: 100%;\n  min-height: 100vh;\n  display: flex;\n  flex-wrap: wrap;\n  justify-content: center;\n  align-items: center;\n}\n\noj-sample-mobile-internal-passcode-screen .dpls-container {\n  width:390px; /* Fix the width for the center passcode content */\n  display: flex;\n  flex-direction: column;\n}\n\noj-sample-mobile-internal-passcode-screen .dpls-appname {\n  font-size: 3rem;\n  text-align:center;\n}\n\noj-sample-mobile-internal-passcode-screen .dpls-appname > div {\n  font-weight: 400;\n  padding-top: 4px;\n\n}\n\noj-sample-mobile-internal-passcode-screen .dpls-passcode-area {\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  flex-direction: column;\n  text-align: center;\n}\n\noj-sample-mobile-internal-passcode-screen .dpls-passcode-input-area {\n  display: flex;\n  flex-direction: row;\n  align-items: center;\n  width: 100%;\n}\n\noj-sample-mobile-internal-passcode-screen .dpls-passcode-input-element {\n  width: 75%;\n  display: flex;\n  justify-content: flex-end;\n}\n\noj-sample-mobile-internal-passcode-screen .dpls-passcode-input-element .oj-inputpassword.oj-read-only .oj-inputpassword-input {\n  letter-spacing: 20px;\n  color: white;\n  font-size: 1.5rem;\n  text-align:center;\n}\n\noj-sample-mobile-internal-passcode-screen .dpls-keypad {\n  display: flex;\n  flex-wrap: wrap;\n  justify-content: center;\n}\n\noj-sample-mobile-internal-passcode-screen .dpls-keypad-row {\n  display: flex;\n  justify-content: space-around;\n  flex-wrap: nowrap;\n  width: 100%;\n  margin: 10px;\n}\n\noj-sample-mobile-internal-passcode-screen .dpls-dummy-btn {\n  height: 80px;\n  width: 70px; /* Find out why this has to be 10 px less */\n}\n\noj-sample-mobile-internal-passcode-screen .dpls-round-btn {\n  border: solid 1px;\n  border-color: #82B9E7;\n  border-radius: 50%;\n  font-size: 2.5rem;\n  cursor:default;\n  height: 80px;\n  width: 80px;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n}\n\noj-sample-mobile-internal-passcode-screen .dpls-round-btn:hover {\n  background-color:#76b8e1;\n  border-color: white;\n}\n\noj-sample-mobile-internal-passcode-screen .dpls-delete-btn-container {\n  display: flex;\n  align-items: center;\n  justify-content: center;\n}\n\noj-sample-mobile-internal-passcode-screen .dpls-white-text {\n  color:white;\n}\n\noj-sample-mobile-internal-passcode-screen .dpls-red-text {\n  color:#cc0000;\n}\n\noj-sample-mobile-internal-passcode-screen .dpls-white-text .oj-button-button > .oj-button-label > .oj-button-text {\n  color:white;\n}\n\n\n');

//# sourceMappingURL=loader.js.map