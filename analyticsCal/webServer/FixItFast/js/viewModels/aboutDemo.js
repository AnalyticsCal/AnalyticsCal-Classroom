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
define(['appUtils'],
  function(appUtils) {
    function aboutDemo() {
      var self = this;
      self.transitionCompleted = function() {
        appUtils.setFocusAfterModuleLoad('startBtn');
      }
    }
    return aboutDemo;
  });
