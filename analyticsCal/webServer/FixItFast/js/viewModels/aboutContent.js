/**
 * @license
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
/**
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
'use strict';
define(['appController', 'ModuleHelper',
        'ojs/ojmodule-element',
        'ojs/ojpopup', 'ojs/ojknockout'], function(app, moduleHelper) {

  function aboutContent(params) {
    var self = this;
    self.toggleDrawer = app.toggleDrawer;
    var aboutListItems = [{id: 'aboutDemo', title: '', label: 'About Demo' },
                          {id: 'privacyPolicy', title: 'Oracle Privacy Policy', label: 'Oracle Privacy Policy' }];


    var routerConfigOptions = {
      'aboutList': { label: 'About', isDefault: true },
      'aboutDemo': { label: 'About Demo' }
    };

    self.router = params.parentRouter.createChildRouter('aboutContent').configure(routerConfigOptions);

    self.optionChange = function(event) {
      var value = event.detail.value;
      if (!value || !value[0])
        return;

      if (value[0] === 'privacyPolicy') {
        params.goToPrivacyPolicy();
        return;
      }

      self.router.go('aboutDemo');
    };

    var moduleParams = {
      'list': aboutListItems,
      'optionChange': self.optionChange
    }

    moduleHelper.setupModuleWithObservable(self, 'moduleConfig', self.router.stateId, moduleParams);
    moduleHelper.setupModuleCaching(self);

    var animationOptions = {
      'aboutList': 'navParent',
      'aboutDemo': 'navChild',
    }
    moduleHelper.setupModuleAnimations(self, animationOptions, self.router.stateId, 'aboutList');

    self.connected = function() {
      oj.Router.sync();
    };

    // dispose about page child router
    self.disconnected = function() {
      self.router.dispose();
    };

    self.goBack = function() {
      self.router.go('aboutList');
    }

    // open social links popup
    self.openPopup = function() {
      var popup = document.getElementById('aboutPopup');
      popup.position = {
        "my": {
          "horizontal": "center",
          "vertical": "top"
        },
        "at": {
          "horizontal": "center",
          "vertical": "top + 50"
        },
        "of": ".oj-hybrid-applayout-content",
        "offset": {
          "x": 0,
          "y": 30
        }
      };

      // place initial focus on the popup instead of the first focusable element
      popup.initialFocus = 'popup';

      return popup.open('#profile-action-btn');
    };
  }

  return aboutContent;
});
