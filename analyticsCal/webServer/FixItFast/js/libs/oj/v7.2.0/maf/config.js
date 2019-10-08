/**
 * config for non-debug libraries
 */

requirejs.config({
  // Path mappings for the logical module names
  paths: {
    'knockout': 'libs/knockout/knockout-3.5.0',
    'jquery': 'libs/jquery/jquery-3.4.1.min',
    'jqueryui-amd': 'libs/jquery/jqueryui-amd-1.12.1.min',
    'ojs': 'libs/oj/v7.2.0/min',
    'ojL10n': 'libs/oj/v7.2.0/ojL10n',
    'ojtranslations': 'libs/oj/v7.2.0/resources',
    'signals': 'libs/js-signals/signals.min',
    'touchr': 'libs/touchr/touchr',
    'text': 'libs/require/text',
    'promise': 'libs/es6-promise/es6-promise.min',
    'hammerjs': 'libs/hammer/hammer-2.0.8.min',
    'ojdnd': 'libs/dnd-polyfill/dnd-polyfill-1.0.0.min'
  },
  // Shim configurations for modules that do not expose AMD
  shim: {
    'jquery': {
      exports: ['jQuery', '$']
    }
  }
});
