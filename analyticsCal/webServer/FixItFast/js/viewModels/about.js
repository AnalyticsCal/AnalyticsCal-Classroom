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
define(['ModuleHelper',
        'ojs/ojmodule-element'],
  function(moduleHelper) {
    function about(params) {
      var self = this;

      // add aboutList as default state on child router
      var routerConfigOptions = {
        'aboutContent': { label: 'About', isDefault: true },
        'privacyPolicy': { label: 'Oracle Privacy Policy' },
      };

      self.router = params.parentRouter.createChildRouter('about').configure(routerConfigOptions);

      self.goToPrivacyPolicy = function() {
        self.router.go('privacyPolicy');
      };

      self.goToAboutContent = function() {
        self.router.go('aboutContent');
      };

      var moduleParams = {
        'goToPrivacyPolicy': self.goToPrivacyPolicy,
        'goToAboutContent': self.goToAboutContent,
        'parentRouter': self.router
      }

      moduleHelper.setupModuleWithObservable(self, 'moduleConfig', self.router.stateId, moduleParams);
      moduleHelper.setupModuleCaching(self);

      var animationOptions = {
        'aboutContent': 'navParent',
        'privacyPolicy': 'navChild'
      }
      moduleHelper.setupModuleAnimations(self, animationOptions, self.router.stateId, 'aboutContent');

      self.connected = function() {
        oj.Router.sync();
      };

      // dispose about page child router
      self.disconnected = function() {
        self.router.dispose();
      };
    }

    return about;

  });
