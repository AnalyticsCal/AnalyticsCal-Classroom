/**
 * @license
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
/**
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */

define(['ojs/ojcore', 'jquery', 'knockout'], function (oj, $, ko) {
  function connectionMessageViewModel(app) {
    var self = this;

    // connection change event
    // cordova-plugin-network-information plugin is needed for hybrid app
    if (typeof Connection != "undefined") {
      document.addEventListener('online',  onlineHandler);
      document.addEventListener('offline', offlineHandler);
    } else {
      // add online and offline event handler for web app
      window.addEventListener('online',  onlineHandler);
      window.addEventListener('offline', offlineHandler);
    }


    var MESSAGES = {
      'online': 'You are connected to network.',
      'offline': 'You are not connected to network.'
    };

    self.isOnline = ko.observable(true);
    self.message = ko.observable()

    var currentTimer;

    // toggle between primary message and secondary message
    self.toggleMessageContent = function(firstText, secondText) {
      self.message(firstText);
      currentTimer = window.setTimeout(function () {
        self.message(secondText);
        self.toggleMessageContent(secondText, firstText);
      }, 2000)
    }

    function onlineHandler() {
      if(self.isOnline()) {
        return;
      }

      // check if there is unsynced requests
      var syncMessage;
      app.offlineController.getSyncLog()
        .then(function (value) {
          if (value.length)
            return Promise.all([value, app.offlineController.sync()]);
          return Promise.resolve([value]);
        }).then(function (results) {
          if (results[0].length) {
            app.offlineController.refreshData(results[0]);
            syncMessage = 'Your updates have been applied.';
          }
        }).catch(function (e) {
          syncMessage = 'Failed to sync your updates.';
        }).finally(function () {
          updateOnlineStatus();
          self.openDrawer(syncMessage);
        });

    }

    function updateOnlineStatus() {
      document.body.classList.remove('offline');

      self.isOnline(true);
      self.message(MESSAGES['online']);
    }

    function offlineHandler() {
      if(!self.isOnline()) {
        return;
      }

      document.body.classList.add('offline');

      self.isOnline(false);
      self.message(MESSAGES['offline']);
      clearTimeout(currentTimer);

      var state = oj.Router.rootInstance.currentState().id;
      if(state === 'incidents' || state === 'createIncident')
        return self.openDrawer('You can create/edit incidents offline.')
      if(state === 'customers')
        return self.openDrawer('You can create/edit customers offline.')
      if(state === 'profile')
        return self.openDrawer('You can edit profile offline.')

      return self.openDrawer();

    }

    self.openDrawer = function (secondMessage) {
      oj.OffcanvasUtils.open({selector: '#connectionDrawer', modality: 'modeless', displayMode: 'overlay', content: '#pageContent' });
      clearTimeout(currentTimer);

      if (secondMessage)
        self.toggleMessageContent(self.message(), secondMessage)
    }

    self.showAfterUpdateMessage = function (errMsg) {
      if (!self.isOnline())
        self.message('Updates will be applied when online.');
      else if (errMsg)
        self.message(errMsg);
      else
        self.message('Your updates have been applied.');

      self.openDrawer();
    }

    self.closeDrawer = function () {
      oj.OffcanvasUtils.close({selector: '#connectionDrawer' });
    };

    // clear timer when drawer is dismissed
    $("#connectionDrawer").on("ojclose", function(event, offcanvas) {
      clearTimeout(currentTimer);
    });

  }
  return connectionMessageViewModel;
})
