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
define(['ojs/ojcore',
        'knockout',
        'appUtils',
        'ojs/ojknockout',
        'ojs/ojlistview',
        'ojs/ojarraytabledatasource'],
  function(oj, ko, appUtils) {
    function aboutList(params) {
      var self = this;
      self.optionChange = params.optionChange;
      // retrieve about items to render the list
      self.aboutOptions = new oj.ArrayTableDataSource(params.list, {idAttribute: 'id'});
      self.selectedItem = ko.observableArray([]);
      self.prefetch = function() {
        self.selectedItem([]);
      }
      self.transitionCompleted = function() {
        appUtils.setFocusAfterModuleLoad('startBtn');
      }
    }
    return aboutList;
  });
