/**
 * @license
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
/**
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */

 // incidents list view viewModel
'use strict';
define(['ojs/ojcore', 'knockout',
        'dataService',
        'appController',
        'appUtils',
        'persist/persistenceStoreManager',
        'ojs/ojknockout',
        'ojs/ojoffcanvas',
        'ojs/ojlistview',
        'ojs/ojswipeactions',
        'ojs/ojpulltorefresh',
        'ojs/ojcheckboxset',
        'ojs/ojarraytabledatasource',
        'ojs/ojpopup',
        'ojs/ojrefresher',
        'ojs/ojanimation',
        'ojs/ojlabel'],
function(oj, ko, data, app, appUtils, persistenceStoreManager) {
  function incidentsTabList(params) {
    var self = this;
    var pullToRefreshInProgress = false;
    self.closePopup = params.closePopup;

    self.refreshIncidents = function() {
      pullToRefreshInProgress = true;
      return new Promise(function(resolve, reject) {
        // check for new incidents
        data.getIncidents()
          .then(function(response) {
            processIncidentsData(response, resolve);
          })
          .fail(function(response){
            reject("Failed to get incidents");
          });
      }).then(function() {
        pullToRefreshInProgress = false;
      }).catch(function() {
        pullToRefreshInProgress = false;
      });
    };

    var updateIncidentsList = function (response) {
      processIncidentsData(response.detail);
      params.incidentList(response.detail);
    };

    var updateBarCharData = function (response) {
      params.barChartResultMetrics(JSON.parse(response.detail).metrics);
    }

    var updatePieChartData = function (response) {
      params.pieChartResult(JSON.parse(response.detail));
    }

    function doOneTimeActivities() {
      if (self.alreadyConnected)
        return;

      self.alreadyConnected = true;
      document.getElementById('page').addEventListener('onIncidentsUpdated', updateIncidentsList);
      //Adding event listener to update module parameters
      document.getElementById('page').addEventListener('onHistoryStatsUpdated', updateBarCharData);
      document.getElementById('page').addEventListener('onIncidentStatsUpdated', updatePieChartData);

      self.onlineStateChangeSubscription = app.subscribeForDeviceOnlineStateChange(function() {
        document.getElementById('incidentsListView').refresh();
      });
      appUtils.adjustContentPadding();
    }

    self.prefetch = function() {
      return new Promise(function(resolve, reject) {
        processIncidentsData(params.incidentList(), resolve);
      })
    }

    self.connected = function() {
      return doOneTimeActivities();
    };

    self.transitionCompleted = function() {
      var addIncidentBtn = document.getElementById('addIncident');

      // When we navigate directly to customerDetails from incident, this dom is not initialized.
      if (addIncidentBtn) {
        oj.Context.getContext(addIncidentBtn).getBusyContext().whenReady().then(function () {
          // invoke zoomIn animation on floating action button
          var animateOptions = { 'delay': 0, 'duration': '0.3s', 'timingFunction': 'ease-out' };
          oj.AnimationUtils['zoomIn'](addIncidentBtn, animateOptions);
        });
      }
    };

    self.disconnected = function () {
      // Store scroll position
      localStorage.setItem("incidents-scroll-top",  self.scrollTop());

      document.getElementById('page').removeEventListener('onIncidentsUpdated', updateIncidentsList);
      document.getElementById('page').removeEventListener('onStatsUpdated', updateBarCharData);
      document.getElementById('page').removeEventListener('onIncidentStatsUpdated', updatePieChartData);
      // un-register swipe to reveal for all list items
      var incidentsListView = document.getElementById("incidentsListView");
      if (incidentsListView) {
        incidentsListView.querySelectorAll(".demo-item-marker").forEach(function(ele) {
          var startOffcanvas = ele.querySelector(".oj-offcanvas-start");
          var endOffcanvas = ele.querySelector(".oj-offcanvas-end");

          oj.SwipeToRevealUtils.tearDownSwipeActions(startOffcanvas);
          oj.SwipeToRevealUtils.tearDownSwipeActions(endOffcanvas);
        });
      }
      if (self.onlineStateChangeSubscription) {
        self.onlineStateChangeSubscription.dispose();
        self.onlineStateChangeSubscription = undefined;
      }

      self.alreadyConnected = false;
    }

    function processIncidentsData(response, resolve) {
      var incidentsData = JSON.parse(response);
      self.lastUpdate = incidentsData.lastUpdate;

      var unreadIncidentsNum = 0;

      incidentsData.result.forEach(function(incident){
        incident.statusObservable = ko.observable(incident.status);
        incident.formattedCreatedOn = appUtils.formatTimeStamp(incident.createdOn).date;
        if(!incident.read)
          unreadIncidentsNum++;
      });

      app.unreadIncidentsNum(unreadIncidentsNum);

      incidentsData.result.sort(function(a, b) {
        return (a.createdOn < b.createdOn) ? 1 : (a.createdOn > b.createdOn) ? -1 : 0;
      });

      persistenceStoreManager.openStore('incidents').then(function (store) {
        store.keys().then(function (keys) {
          incidentsData.result.forEach(function (incident) {
            incident.cached = false;
            keys.forEach(function (key) {
              if(key.indexOf(incident.id) > -1) {
                incident.cached = true
              }
            })

          })

          self.allIncidents = incidentsData.result;

          var results = self.filterIncidents();

          // show message when no data is available.
          if(results.length === 0) {
            document.getElementById("incidentsListView").translations.msgNoData = "new message";
          }

          // update observable
          self.filteredIncidents(results);
          // trigger listview to reload (skipping model change event animation)
          self.incidentsTableData.reset();

          var listView = document.getElementById('incidentsListView');
          oj.Context.getContext(listView).getBusyContext().whenReady().then(function () {
            self.setupSwipeActions();
          });

          if (resolve)
            resolve();
        })
      })
    }

    self.scrollElem = navigator.userAgent.search(/Firefox|Trident|Edge/g)  > -1 ? document.body.parentElement : document.body;
    self.scrollTop = ko.observable(0);

    self.priorityFilterArr = ko.observable(['high', 'normal', 'low']);
    self.statusFilterArr = ko.observable(['open', 'accepted', 'closed']);

    self.allIncidents = [];

    self.filteredIncidents = ko.observableArray([]);
    self.incidentsTableData = new oj.ArrayTableDataSource(self.filteredIncidents, { idAttribute: 'id' });

    self.filterIncidents = function() {
      return self.allIncidents.filter(function(incident) {
        return self.priorityFilterArr().indexOf(incident.priority) > -1 && self.statusFilterArr().indexOf(incident.statusObservable()) > -1;
      });
    };

    // update incidents list when priority or status filter changes
    self.priorityFilterArr.subscribe(function(newValue) {
      var filteredResults = self.filterIncidents();
      self.filteredIncidents(filteredResults);
    });

    self.statusFilterArr.subscribe(function(newValue) {
      var filteredResults = self.filterIncidents();
      self.filteredIncidents(filteredResults);
    });

    self.incidentSelectable = function(itemContext) {
      return app.isDeviceOnline() || itemContext.data.cached;
    }

    self.incidentSelected = function(event) {
      if (pullToRefreshInProgress)
        return;

      var value = event.detail.value;
      if (!value || !value[0])
        return;

      event.preventDefault();
      params.incidentsTabListAnimation(null);
      app.goToIncident(value[0], 'incidentsTabList');
    };

    self.goToAddIncident = function() {
      app.goToCreateIncident();
    };

    self.setupSwipeActions = function() {
      // register swipe to reveal for all new list items
      var incidentsListView = document.getElementById("incidentsListView");
      if (incidentsListView) {
        incidentsListView.querySelectorAll(".demo-item-marker").forEach(function(ele) {
          var startOffcanvas = ele.querySelector(".oj-offcanvas-start");
          var endOffcanvas = ele.querySelector(".oj-offcanvas-end");

          // setup swipe actions
          oj.SwipeToRevealUtils.setupSwipeActions(startOffcanvas);
          oj.SwipeToRevealUtils.setupSwipeActions(endOffcanvas);

        });
      }

      // Restore scroll position
      self.scrollTop(localStorage.getItem("incidents-scroll-top"));
    };

    self.closeToolbar = function(item) {
      var toolbarSelector = "li#"+item.id + " .oj-swipetoreveal";
      var drawer = {"displayMode": "push", "selector": toolbarSelector};

      oj.OffcanvasUtils.close(drawer);
    };

    self.handleAction = function(event, model) {
      var action = event.target.value,
        dataModel = model.data;

      if (!dataModel || !dataModel.id) {
        return;
      }

      self.closeToolbar(dataModel);

      var index = self.allIncidents.map(function(e) { return e.id; }).indexOf(dataModel.id);
      self.allIncidents[index].statusObservable(action);

      data.updateIncident(dataModel.id, {status: action}).then(function(response) {
        // update success
        // re-apply filter to incidents after changing status
        self.filterIncidents();
      }).fail(function(response){
        oj.Logger.error('Failed to update incident.', response)
        app.connectionDrawer.showAfterUpdateMessage();
      });
    };
  }

  return incidentsTabList;

});
