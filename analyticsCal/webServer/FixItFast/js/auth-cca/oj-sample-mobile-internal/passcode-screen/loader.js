/**
 * @license
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
/**
  Copyright (c) 2015, 2018, Oracle and/or its affiliates.
  The Universal Permissive License (UPL), Version 1.0
*/
define(['ojs/ojcomposite', 'text!./passcode-screen-view.html',
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