/**
 * @license
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
({
  baseUrl: "js",
  appDir: "../",
  dir: "rjs_built",
  bundlesConfigOutFile: 'js/main.js',
  modules: [
    {
      name: "rjs_bundles/listBundle",
      create: true,
      include: ['ojs/ojswipetoreveal', 'ojs/ojoffcanvas', 'ojs/ojpulltorefresh', 'ojs/ojlistview', 'ojs/ojarraytabledatasource'],
      exclude: ['jquery']
    },
    {
      name: "rjs_bundles/mapviewBundle",
      create: true,
      include: ['oraclemapviewer', 'oracleelocation'],
      exclude: ['jquery']
    }
  ],
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
    'touchr': 'libs/touchr/touchr'
  },
  //endinjector
  optimize: "none"
})
