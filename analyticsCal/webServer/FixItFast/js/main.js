/**
 * @license
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
/**
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */

/**
 * Example of Require.js boostrap javascript
 */
'use strict';
requirejs.config({
  // Path mappings for the logical module names
  paths:
  //injector:mainReleasePaths
  {
    'knockout': 'libs/knockout/knockout-3.5.0',
    'mapping': 'libs/knockout/knockout.mapping-latest',
    'jquery': 'libs/jquery/jquery-3.4.1.min',
    'jqueryui-amd': 'libs/jquery/jqueryui-amd-1.12.1.min',
    'promise': 'libs/es6-promise/es6-promise.min',
    'hammerjs': 'libs/hammer/hammer-2.0.8.min',
    'ojdnd': 'libs/dnd-polyfill/dnd-polyfill-1.0.0.min',
    'ojs': 'libs/oj/v7.2.0/min',
    'ojL10n': 'libs/oj/v7.2.0/ojL10n',
    'ojtranslations': 'libs/oj/v7.2.0/resources',
    'signals': 'libs/js-signals/signals.min',
    'text': 'libs/require/text',
    'oraclemapviewer': 'libs/oraclemapsv2',
    'oracleelocation': 'libs/oracleelocationv3',
    'customElements': 'libs/webcomponents/custom-elements.min',
    'css': 'libs/require-css/css.min',
    'touchr': 'libs/touchr/touchr',
    'pouchdb': 'libs/pouchdb/min/pouchdb-6.3.4',
    'pouchfind': 'libs/pouchdb/min/pouchdb.find',
    'persist': 'libs/persist/min',
    'appConfig': 'appConfigExternal',
    'oj-sample-mobile-internal':'auth-cca/oj-sample-mobile-internal'
  }
  //endinjector
});

requirejs.config(
  {
    bundles:
      {
        'listBundle': ['ojL10n', 'ojtranslations/nls/ojtranslations', 'promise', 'ojs/ojcore', 'hammer', 'ojs/ojjquery-hammer',
          'jqueryui-amd/version',  'jqueryui-amd/widget', 'jqueryui-amd/unique-id',
          'jqueryui-amd/keycode', 'jqueryui-amd/focusable', 'jqueryui-amd/tabbable', 'ojs/ojmessaging', 'customElements', 'ojs/ojcomponentcore', 'ojs/ojoffcanvas',
          'ojs/ojswipetoreveal', 'ojs/ojpulltorefresh', 'ojs/ojdomscroller', 'ojs/ojanimation', 'ojs/ojlistview', 'ojs/ojdatasource-common', 'ojs/ojarraytabledatasource'],
        'mapviewBundle': ['oraclemapviewer', 'ojs/oracleelocation']
      }
  }
);

require(['pouchdb'], function (pouchdb) {
  window.PouchDB = pouchdb;
});

/**
 * A top-level require call executed by the Application.
 * Although 'ojcore' and 'knockout' would be loaded in any case (they are specified as dependencies
 * by the modules themselves), we are listing them explicitly to get the references to the 'oj' and 'ko'
 * objects in the callback
 */
require(['ojs/ojcore', 'knockout', 'appController', 'jquery'], function (oj, ko, app, $) {

  $(function() {

    function init() {
      oj.Router.sync().then(function () {
        // bind your ViewModel for the content of the whole page body.
        ko.applyBindings(app, document.getElementById('page'));
      }, function (error) {
        oj.Logger.error('Error in root start: ' + error.message);
      });
    }

    // If running in a hybrid (e.g. Cordova) environment, we need to wait for the deviceready
    // event before executing any code that might interact with Cordova APIs or plugins.
    if ($(document.body).hasClass('oj-hybrid')) {
      document.addEventListener("deviceready", init);
    } else {
      init();
    }

  });

});
