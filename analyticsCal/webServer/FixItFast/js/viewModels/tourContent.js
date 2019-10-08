/**
 * @license
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
/**
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */

 // view model for the tour content with filmstrip
'use strict';
define(['knockout', 'ojs/ojfilmstrip', 'ojs/ojpagingcontrol', 'ojs/ojknockout'], function(ko) {
  function tourContent(params) {
    var self = this;

    self.pagingModel = ko.observable(null);
    self.filmStripOptionChange = params.filmStripOptionChange;

    // todo: need to fix the animation so that the paging model is set before the transition occurs
    self.connected = function() {
      var filmStrip = document.getElementById("filmStrip");
      oj.Context.getContext(filmStrip).getBusyContext().whenReady().then(function () {
        self.pagingModel(filmStrip.getPagingModel());
      });
    }

    self.steps = [
      {
        'title': 'dashboard',
        'description': 'Review a dashboard of your current incidents.',
        'imgSrc': 'css/images/dashboard_image@2x.png',
        'color': '#4493cd'
      },
      {
        'title': 'maps',
        'description': 'Find locations and directions to your customers.',
        'imgSrc': 'css/images/maps_image@2x.png',
        'color': '#FFD603'
      },
      {
        'title': 'incidents',
        'description': 'Check on details about the incident including seeing feed updates and photos.',
        'imgSrc': 'css/images/incidents_image@2x.png',
        'color': '#E5003E'
      },
      {
        'title': 'customers',
        'description': 'Have your customers information easily available.',
        'imgSrc': 'css/images/customers_image@2x.png',
        'color': '#009636'
      }
    ];

    self.getItemInitialDisplay = function(index) {
      return index < 1 ? '' : 'none';
    };

  }
  return tourContent;
});
