/**
 * @license
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
/**
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
define(['ModuleHelper', 'ojs/ojmodule-element'], function(moduleHelper) {
  function privacyPolicy(params) {
    var self = this;

    self.connected = function() {
      // Using app.appUtilities.adjustContentPadding() has ill effect
      // on the outgoing ojmodule transparency
      // Therefore, using local padding adjustment code.
      var header = document.getElementById('policyContentTop');
      var content = document.getElementById('policyContent');
      content.style.paddingTop = header.offsetHeight + 'px';
    }

    // create customer page header settings
    var headerViewModelParams = {
      title: 'Oracle Privacy Policy',
      startBtn: {
        id: 'backBtn',
        click: params.goToAboutContent,
        display: 'icons',
        label: 'Back',
        icons: 'oj-hybrid-applayout-header-icon-back oj-fwk-icon',
        visible: true
      },
      endBtn: {
        visible: false,
      }
    };

    moduleHelper.setupStaticModule(self, 'headerConfig', 'basicHeader', headerViewModelParams);
  }

  return privacyPolicy;
});
