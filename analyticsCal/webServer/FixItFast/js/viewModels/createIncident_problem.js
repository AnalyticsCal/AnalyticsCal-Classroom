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
        'ojs/ojinputtext',
        'ojs/ojarraytabledatasource',
        'ojs/ojradioset',
        'ojs/ojlabel', 'ojs/ojformlayout'], function(oj) {
  function createIncident_problem(params) {
    var self = this;

    var categoryData = [
      {id: 'appliance', title: 'Appliance'},
      {id: 'electrical', title: 'Electrical'},
      {id: 'heatingcooling', title: 'Heating / Cooling'},
      {id: 'plumbing', title: 'Plumbing'},
      {id: 'generalhome', title: 'General Home'}
    ];

    var priorityData = [
      {id: 'high', title: 'High'},
      {id: 'normal', title: 'Normal'},
      {id: 'low', title: 'Low'}
    ];

    self.prefetch = function() {
      self.newIncidentModel = params.newIncidentModel;
      self.priorityList = new oj.ArrayTableDataSource(priorityData, {idAttribute: 'id'});
      self.categoryList = new oj.ArrayTableDataSource(categoryData, {idAttribute: 'id'});
    }
  }

  return createIncident_problem;
});
