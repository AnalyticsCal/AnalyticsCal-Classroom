/**
 * @license
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
/**
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */

// header module viewModel

'use strict';
define(['appUtils', 'ojs/ojbutton', 'ojs/ojknockout'], function(appUtils) {
  function basicHeaderVM(params) {
    var self = this;
    self.title = params.title || '';
    self.startBtn = params.startBtn;
    self.endBtn = params.endBtn;
    self.endBtn.disabled = params.endBtn.disabled || false;

    self.transitionCompleted = function() {
      appUtils.setFocusAfterModuleLoad(self.startBtn.id);
    }
  }
  return basicHeaderVM;
});
