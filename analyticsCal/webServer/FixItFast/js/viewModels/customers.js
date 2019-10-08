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
        'appUtils',
        'persist/persistenceStoreManager',
        'ojs/ojknockout',
        'ojs/ojselectcombobox',
        'ojs/ojindexer',
        'ojs/ojanimation',
        'ojs/ojindexermodeltreedatasource'], function(oj, ko, data, app, appUtils, persistenceStoreManager){
  function customers(params) {
    var self = this, handleSectionClick;
    self.appUtilities = appUtils;
    self.toggleDrawer = app.toggleDrawer;
    self.parentRouter = params.parentRouter;
    self.scrollElem = document.body;
    self.allCustomers = ko.observableArray();
    self.nameSearchValue = ko.observableArray();
    self.nameSearchRawValue = ko.observable();
    self.noResults = ko.observable(false);
    self.isSearchMode = ko.observable(false);
    self.indexerModel = ko.observable(null);
    self.addCustomerVisible = ko.observable(false);

    // filter customers
    self.customers = ko.computed(function() {
      var allCustomers = self.allCustomers();
      if(!allCustomers.data)
        return;

      if(self.nameSearchRawValue() && allCustomers.data.length > 0) {
        var filteredCustomers = [];
        var token = self.nameSearchRawValue().toLowerCase();

        allCustomers.data.forEach(function (node) {
          if(node.firstName.toLowerCase().indexOf(token) === 0 || node.lastName.toLowerCase().indexOf(token) === 0) {
            filteredCustomers.push(node);
          }
        });

        self.noResults(filteredCustomers.length == 0);
        if(filteredCustomers.length) {
          var parsedData =  new oj.IndexerModelTreeDataSource(filteredCustomers, 'id', handleSectionClick,
            {'groupingAttribute': 'firstName', sortComparatorFunction: self.sortCustomers});
          self.indexerModel(parsedData);
        }
      } else {
        self.noResults(false);
        var parsedData = new oj.IndexerModelTreeDataSource(allCustomers.data, 'id', handleSectionClick,
          {'groupingAttribute': 'firstName', sortComparatorFunction: self.sortCustomers});
        self.indexerModel(parsedData);
      }
    });

    self.prefetch = function() {
      return new Promise(function(resolve, reject) {
        data.getCustomers().then(function(response) {
          processCustomers(response, resolve);
        });
      });
    }

    var refreshCustomers = function (response) {
      processCustomers(response.detail);
    };

    function doOneTimeActivities() {
      if (self.alreadyConnected)
        return;

      self.alreadyConnected = true;

      document.getElementById('page').addEventListener('onCustomersUpdated', refreshCustomers);

      self.onlineStateChangeSubscription = app.subscribeForDeviceOnlineStateChange(function() {
        document.getElementById('customerlistview').refresh();
      });

      var listView = document.getElementById('customerlistview');
      oj.Context.getContext(listView).getBusyContext().whenReady().then(function () {
          // adjust content padding top
          appUtils.adjustContentPadding();

          // adjust padding-bottom for indexer
          var topElem = document.getElementsByClassName('oj-applayout-fixed-top')[0];
          var contentElem = document.getElementById('indexer').getElementsByTagName('ul')[0];
          contentElem.style.paddingBottom = topElem.offsetHeight+'px';
          contentElem.style.position = 'fixed';
          contentElem.style.height = '100%';
      });
    }

    self.connected = function() {
      doOneTimeActivities();
    };

    self.transitionCompleted = function() {
      appUtils.setFocusAfterModuleLoad('navDrawerBtn');
      var addCustomerBtn = document.getElementById('addCustomer');

      // When we navigate directly to customerDetails from incident, this dom is not initialized.
      if (addCustomerBtn) {
        oj.Context.getContext(addCustomerBtn).getBusyContext().whenReady().then(function () {
          // invoke zoomIn animation on floating action button
          var animateOptions = { 'delay': 0, 'duration': '0.3s', 'timingFunction': 'ease-out' };
          oj.AnimationUtils['zoomIn'](addCustomerBtn, animateOptions);
        });
      }
    };

    self.disconnected = function() {
      document.getElementById('page').removeEventListener('onCustomersUpdated', refreshCustomers);

      if (self.onlineStateChangeSubscription) {
        self.onlineStateChangeSubscription.dispose();
        self.onlineStateChangeSubscription = undefined;
      }

      self.alreadyConnected = false;
    }

    function processCustomers(response, resolve) {
      var result = JSON.parse(response).result;
      persistenceStoreManager.openStore('customers')
        .then(function (store) {
          store.keys().then(function (keys) {
            result.forEach(function (customer) {
              if(keys.indexOf(customer.id) > -1) {
                customer.cached = true;
              } else {
                customer.cached = false;
              }
            })

            var parsedData = new oj.IndexerModelTreeDataSource(result, 'id', handleSectionClick,
              {'groupingAttribute': 'firstName', sortComparatorFunction: self.sortCustomers});
            self.indexerModel(parsedData);
            self.allCustomers(parsedData);
            if (resolve)
              resolve();
        })
        .catch(function() {
          if (resolve)
            resolve();
        })
        ;
      })
    };

    handleSectionClick = function(section) {
      var self = this;
      return new Promise(function(resolve, reject) {
        section = findAvailableSection(section);
        if (section != null) {
          document.getElementById('customerlistview').scrollToItem({'key': section});
        }
        resolve(section);
      });
    };

    function findAvailableSection(section) {
      var missing = self.indexerModel().getMissingSections();
      if (missing.indexOf(section) > -1) {
        var sections = self.indexerModel().getIndexableSections();
        var index = sections.indexOf(section);
        if (index + 1 < sections.length) {
          section = sections[index + 1];
          return self.findAvailableSection(section);
        } else {
          return null;
        }
      } else {
        return section;
      }
    };


    self.sortCustomers = function(a, b) {
      // sort by first name
      if (a.firstName > b.firstName) {
        return 1;
      }
      if (a.firstName < b.firstName) {
        return -1;
      }

      // else sort by last name
      return (a.lastName > b.lastName) ? 1 : (a.lastName < b.lastName) ? -1 : 0;
    };


    self.itemOnly = function(context) {
      return context['leaf'];
    };

    self.selectTemplate = function(context) {
      var renderer = oj.KnockoutTemplateUtils.getRenderer(context.leaf ? 'item_template' : 'group_template', true);
      return renderer.call(this, context)
    };

    self.getIndexerModel = function() {
      if (self.indexerModel() == null) {
        var listView = document.getElementById('customerlistview');
        var indexerModel = listView.getIndexerModel();
        self.indexerModel(indexerModel);
      }
    };

    // go to create customer page
    self.goToAddCustomer = function() {
      self.parentRouter.go('customerCreate');
    };

    self.customerSelectable = function(itemContext) {
      return app.isDeviceOnline() || itemContext.data.cached;
    }

    // handler for drill in to customer details
    self.customerSelected = function(event) {
      var value = event.detail.value;
      if (!value || !value[0])
        return;

      self.parentRouter.go('customerDetails/' + value[0]);
    };

    self.goToSearchMode = function() {
      self.isSearchMode(true);
      document.getElementById("inputSearch").focus();
    };

    self.exitSearchMode = function() {
      self.isSearchMode(false);
      self.clearSearch();
    };

    self.clearSearch = function() {
      self.nameSearchValue([]);
      self.nameSearchRawValue('');
      self.noResults(false);
    };
  }

  return customers;
});
