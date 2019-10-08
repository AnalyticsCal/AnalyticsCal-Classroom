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
define(['ojs/ojcore', 'knockout',
        'dataService',
        'appController',
        'ImageHelper',
        'appUtils',
        'ojs/ojknockout',
        'ojs/ojlistview',
        'ojs/ojarraytabledatasource',
        'ojs/ojinputtext',
        'ojs/ojrefresher'], function(oj, ko, data, app, imageHelper, appUtils) {
  function incidentTabActivity(params) {

    var self = this;
    self.isReadOnlyMode = app.isReadOnlyMode;
    self.appUtilities = appUtils;
    self.postBtnDisabled = ko.observable(true);

    // retrieve incident id
    self.incidentId = params.parentRouter.parent.currentState().id;

    self.scrollElem = document.body;

    self.allActivities = ko.observableArray([]);
    self.dataSource = new oj.ArrayTableDataSource(self.allActivities, { idAttribute: 'id' });

    function getActivities() {
      // check for new activities
      return new Promise(function (resolve, reject) {
        data.getIncidentActivities(self.incidentId)
          .then(function(response) {
            var data = JSON.parse(response);
            var results = data.activities;
            self.lastUpdate = data.lastUpdate;
            processActivities(results);
            resolve();
          })
          .catch(function (e) {
            reject(e);
          });
      });
    }

    function processActivities(results) {
      results.sort(function(a, b) {
        return (a.createdOn < b.createdOn) ? 1 : (a.createdOn > b.createdOn) ? -1 : 0;
      });

      self.allActivities(results);

      self.dataSource.reset();

      if(results.length === 0) {
        var activityListView = document.getElementById('activityListView');
        activityListView.translations.msgNoData = 'No Activity';
        activityListView.refresh();
      }
    }

    self.refreshList = function() {
      return getActivities();
    };

    self.prefetch = function() {
      return getActivities();
    }

    self.connected = function () {
      document.getElementById('page').addEventListener('onActivitiesUpdated', refreshActivities);
      // adjust content padding top
      appUtils.adjustContentPadding();
      imageHelper.registerImageListeners(app, 'upload-activity-pic', self.imageSrc, self, 'changePhoto');
    }

    self.disconnected = function () {
      document.getElementById('page').removeEventListener('onActivitiesUpdated', refreshActivities);
    }

    var refreshActivities = function (response) {
      var data = JSON.parse(response.detail);
      var results = data.activities;
      self.lastUpdate = data.lastUpdate;
      processActivities(results);
    }

    self.activityText = ko.observable();
    self.imageSrc = ko.observable();

    // post to activity list
    self.postActivity = function() {
      imageHelper.loadImage(self.imageSrc())
        .then(function(base64Image) {
          return data.postIncidentActivity(self.incidentId, self.activityText(), base64Image);
        })
        .then(function(response) {
          self.activityText('');
          self.imageSrc('');
          document.getElementById('upload-activity-pic').value = '';
          self.allActivities.unshift(JSON.parse(response));
          app.connectionDrawer.showAfterUpdateMessage();
        })
        .catch(function(err) {
          var errMsg = 'Failed to post activity';
          oj.Logger.error(errMsg, err);
          app.connectionDrawer.showAfterUpdateMessage(errMsg);
        });
    };

    self.validatePostBtnState = function(event) {
      if (self.isReadOnlyMode)
        return;

      var text = event.target.value.trim();
      if ((text && !self.postBtnDisabled()) || (!text && self.postBtnDisabled()))
        return;

      self.postBtnDisabled(!self.postBtnDisabled());
    };
  }

  return incidentTabActivity;
});
