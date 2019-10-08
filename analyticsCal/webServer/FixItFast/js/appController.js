/**
 * @license
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
/**
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */

// Application level setup including router, animations and other utility methods

'use strict';
define(['ojs/ojcore', 'knockout', 'dataService', 'mapping', 'PushClient', 'OfflineController',
        'ConnectionDrawer', 'ModuleHelper', 'ImageHelper', 'oj-sample-mobile-internal/common/auth-error-translations',
        'oj-sample-mobile-internal/local-authentication/loader',
        'ojs/ojmodule-element', 'ojs/ojknockout', 'ojs/ojnavigationlist', 'ojs/ojoffcanvas', 'ojs/ojrouter',
        'ojs/ojmoduleanimations', 'ojs/ojmessages'],
function (oj, ko, data, mapping, PushClient, OfflineController, ConnectionDrawer, moduleHelper, imageHelper, authErrTrsl) {

  oj.Router.defaults['urlAdapter'] = new oj.Router.urlParamAdapter();

  var router = oj.Router.rootInstance;

  // Root router configuration
  router.configure({
    'tour': { label: 'Tour', isDefault: true},
    'signin': { label: 'Sign In'},
    'incidents': { label: 'Incidents' },
    'incident': { label: 'Incident' },
    'createIncident': { label: 'Create an Incident' },
    'customers': { label: 'Customers' },
    'customerDetails': { label: 'Customer Details' },
    'customerCreate': { label: 'Create a customer' },
    'profile': { label: 'Profile' },
    'settings': { label: 'Settings' },
    'about': { label: 'About'}
  });

  var darkBackgroundViews = ["tour", "signin", "about", "aboutContent", "aboutDemo", "aboutList"];

  function AppControllerViewModel() {

    ko.mapping = mapping;

    var self = this;

    // push client
    self.pushClient = new PushClient(self);

    //offline controller
    self.offlineController = new OfflineController(self);

    self.connectionDrawer = new ConnectionDrawer(self);

    self.unreadIncidentsNum = ko.observable();

    self.router = router;

    // App messages holder
    self.appMessages = ko.observableArray();
    self.appMsgPos = ko.observable({
      'my': {'vertical' :'top', 'horizontal': 'end'},
      'at': {'vertical': 'top', 'horizontal': 'end'},
      'of': 'window'
    });

    // drill in and out animation
    var platform = oj.ThemeUtils.getThemeTargetPlatform();

    // disable buttons for post/patch/put
    self.isReadOnlyMode = true;

    // set default connection to MCS backend
    self.usingMobileBackend = ko.observable();
    self.usingMobileBackend.subscribe(function(newValue) {
      data.setUseMobileBackend(newValue);
    });

    // Assume online mode to start with
    self.usingMobileBackend(true);

    // Load user profile
    self.userProfileModel = ko.observable();
    var initialProfile;

    self.getUserProfile = function () {
      return new Promise(function(resolve, reject){
        data.getUserProfile().then(function(response){
          processUserProfile(response, resolve, reject);
        }).catch(function(response){
          oj.Logger.warn('Failed to connect to MCS. Loading from local data.');
          self.usingMobileBackend(false);
          //load local profile data
          data.getUserProfile().then(function(response){
            processUserProfile(response, resolve, reject);
          });
        });
      });
    }

    self.isDeviceOnline = function() {
      return self.connectionDrawer.isOnline();
    }

    self.subscribeForDeviceOnlineStateChange = function(callback) {
      return self.connectionDrawer.isOnline.subscribe(callback);
    }

    function processUserProfile(response, resolve, reject) {
      var result = JSON.parse(response);

      if (result) {
        initialProfile = result;
        self.userProfileModel(ko.mapping.fromJS(result));
        resolve(self.userProfileModel);
        return;
      }

      // This won't happen in general, because then that means the entire offline data loading is broken.
      var message = 'Failed to load user profile both online and offline.';
      oj.Logger.error(message);
      reject(message);
    }

    self.updateProfileData = function(updatedModel) {
      imageHelper.loadImage(updatedModel().photo())
        .then(function(base64Image) {
          updatedModel().photo = base64Image;
          initialProfile = ko.mapping.toJS(updatedModel);
          return data.updateUserProfile(initialProfile)
        })
        .then(function() {
          self.getUserProfile();
        })
        .catch(function(response){
          oj.Logger.error(response);
          self.connectionDrawer.showAfterUpdateMessage('Failed to save user profile');
        });
    };

    // Revert changes to user profile
    self.revertProfileData = function() {
      self.userProfileModel(ko.mapping.fromJS(initialProfile));
    };

    // initialise spen plugin
    self.spenSupported = ko.observable(false);
    function isSpenSupported() {
      self.spenSupported(true);
    }
    function initialise() {
      if (window.samsung) {
        samsung.spen.isSupported(isSpenSupported, spenFail);
      }
    }
    function spenFail(error) {
      oj.Logger.error(error);
    }
    initialise();


    var prevPopupOptions = null;

    self.setupPopup = function(imgSrc) {

      // Define the success function. The popup launches if the success function gets called.
      var success = function(imageURI) {

        if(imageURI.length > 0) {
          // SPen saves image to the same url
          // add query and timestamp for versioning of the cache so it loads the latest
          imageURI = imageURI + '?' + Date.now();
          imgSrc(imageURI);
        }

      }

      // Define the faliure function. An error message displays if there are issues with the popup.
      var failure = function(msg) {
        oj.Logger.error(msg);
      }

      // If there are any previous popups, remove them first before creating a new popup
      if (prevPopupOptions !== null){
        // Call the removeSurfacePopup method from the SPen plugin
        samsung.spen.removeSurfacePopup(prevPopupOptions.id, function() { }, failure);
      }

      var popupOptions = {};
      popupOptions.id = "popupId";

      popupOptions.sPenFlags = 0;

      // strip off suffix from compressed image
      var imageURL;
      if(imgSrc().lastIndexOf('?') > -1) {
        imageURL = imgSrc().slice(0, imgSrc().lastIndexOf('?'));
      } else {
        imageURL = imgSrc();
      }

      popupOptions.imageUri = imageURL;
      popupOptions.imageUriScaleType = samsung.spen.IMAGE_URI_MODE_STRETCH;
      popupOptions.sPenFlags = samsung.spen.FLAG_PEN | samsung.spen.FLAG_ERASER | samsung.spen.FLAG_UNDO_REDO |
                            samsung.spen.FLAG_PEN_SETTINGS;
      popupOptions.returnType = samsung.spen.RETURN_TYPE_IMAGE_URI;

      //Launch the popup
      prevPopupOptions = popupOptions;
      samsung.spen.launchSurfacePopup(popupOptions, success, failure);

    };

    self.goToCustomers = function(id) {
      self.router.go('customers');
    };

    // Navigate to customer by id
    self.goToCustomer = function(id) {
      self.router.go('customerDetails/' + id);
    };

    self.goToCustomerFromIncident = function(id, incidentId) {
      self.fromIncidentId = incidentId;
      self.goToCustomer(id);
    };

    // Navigate to incident by id
    self.goToIncident = function(id, from) {
      self.router.go('incident/' + id);
      self.fromIncidentsTab = from;
    };

    self.goToIncidentFromCustomer = function() {
      // Use the existing value for fromIncidentsTab
      self.goToIncident(self.fromIncidentId, self.fromIncidentsTab);
      self.fromIncidentId = undefined;
    };

    self.goToSignIn = function() {
      self.router.go('signin');
    };

    self.goToIncidents = function() {
      var destination = self.fromIncidentsTab || 'incidentsTabList';
      self.router.go('incidents/' + destination);
    };

    self.goToCreateIncident = function() {
      self.fromIncidentsTab = 'incidentsTabList';
      self.router.go('createIncident');
    };

    self.toggleDrawer = function () {
      self.getUserProfile().then(function() {
        oj.OffcanvasUtils.toggle({selector: '#navDrawer', modality: 'modal', content: '#pageContent' });
      })
    };

    self.validNavListStates = ['incidents', 'customers', 'profile', 'settings', 'about'];

    self.beforeCloseDrawer = function(event, vm) {
      var key = event.detail.key;

      if (key === 'signout') {
        event.preventDefault()
        vm.goToSignIn();
        vm.signIn();
        return;
      }

      if (self.validNavListStates.indexOf(key) === -1) {
        event.preventDefault();
        vm.closeDrawer();
        return;
      }
    };

    self.closeDrawer = function () {
      oj.OffcanvasUtils.close({selector: '#navDrawer', modality: 'modal', content: '#pageContent' });
    };

    self.bottomDrawer = { selector: '#bottomDrawer', modality: 'modal', content: '#pageContent', displayMode: 'overlay' };

    self.openBottomDrawer = function(imageObject) {
      self.updateProfilePhoto = function(sourceType) {
        // Save image as file and share the URL by default.
        // We do not want to load many base64 images into memory and suffocate the app.
        var cameraOptions = {
          quality: 50,
          destinationType: Camera.DestinationType.FILE_URI,
          sourceType: sourceType,
          encodingType: 0,     // 0=JPG 1=PNG
          correctOrientation: true,
          targetHeight: 2000,
          targetWidth: 2000
        };

        navigator.camera.getPicture(function(imgData) {
          imageObject(imgData)
        }, function(err) {
          oj.Logger.error(err);
        }, cameraOptions);

        return self.closeBottomDrawer();
      };

      return oj.OffcanvasUtils.open(self.bottomDrawer);
    };

    self.closeBottomDrawer = function() {
      return oj.OffcanvasUtils.close(self.bottomDrawer);
    };

    // Setup moduleConfig
    var moduleParams = {
      'parentRouter': self.router
    }

    var applyStausBarStyle = function(stateId) {
      if (!window.StatusBar)
        return;

      var styleFunction = 'styleDefault';
      if (darkBackgroundViews.indexOf(stateId) > -1)
        styleFunction = 'styleLightContent';

      if (self.currentStatusBarStyle === styleFunction)
        return;

      self.currentStatusBarStyle = styleFunction;
      window.StatusBar[styleFunction]();
    }

    // moduleHelper.setupModuleCaching(self);
    moduleHelper.setupModuleWithObservable(self, 'moduleConfig', self.router.stateId, moduleParams);
    oj.Router.transitionedToState.add(function(result) {
      if (!result.hasChanged)
        return;
      if (!result.newState || !result.oldState)
        return;
      var newId = result.newState.id;
      var oldId = result.oldState.id;

      applyStausBarStyle(newId);

      if (newId === 'customerDetails' && oldId === 'incident') {
        self.incidentAnimation('navParent');
        return;
      }

      if ((newId === 'incident' || newId === 'createIncident') && oldId === 'incidents') {
        self.incidentAnimation('navChild');
        self.incidentsAnimation('navParent');
        return;
      }

      if ((newId === 'customerDetails' || newId === 'customerCreate') && oldId === 'customers') {
        self.customersAnimation('navParent');
        return;
      }

      if (newId == 'incidents' && oldId !== 'incident' && oldId !== 'createIncident') {
        self.incidentsAnimation(null);
        return;
      }

      if (newId == 'customers' && oldId !== 'customerDetails' && oldId !== 'customerCreate') {
        self.customersAnimation(null);
        return;
      }
    });

    // Setup module animations
    self.incidentAnimation = ko.observable('navChild');
    self.incidentsAnimation = ko.observable();
    self.customersAnimation = ko.observable();

    self.moduleTransitionStarted = function(event) {
      var topElems = document.getElementsByClassName('oj-applayout-fixed-top');
      for (var i = 0; i < topElems.length; i++)
        topElems[i].style.zIndex = 0;
    }

    self.moduleTransitionEnded = function(event) {
      var topElems = document.getElementsByClassName('oj-applayout-fixed-top');
      for (var i = 0; i < topElems.length; i++)
        topElems[i].style.zIndex = '';
    }

    var animationOptions = {
      'tour': null,
      'incidents': self.incidentsAnimation,
      'signin': null,
      'customers': self.customersAnimation,
      'customerDetails': 'navChild',
      'customerCreate': 'navChild',
      'profile': null,
      'about': null,
      'incident': self.incidentAnimation,
      'settings': null,
      'createIncident': 'navChild'
    };

    moduleHelper.setupModuleAnimations(self, animationOptions, self.router.stateId, 'tour');
    self.setupLocalAuthHeader();
    self.initLocalAuth();
  }

  AppControllerViewModel.prototype.setPageContentModuleVisibility = function(visible) {
    this.pageContentModuleDisplay(visible ? '' : 'none');
  };

  AppControllerViewModel.prototype.showLocalAuthConfig = function() {
    document.getElementById("localAuth").launchConfigureScreen();
    this.setPageContentModuleVisibility(false);
  };

  AppControllerViewModel.prototype.goBackFromLocalAuthConfig = function() {
    document.getElementById("localAuth").dismissConfigureScreen();
    this.setPageContentModuleVisibility(true);
  };

  AppControllerViewModel.prototype.setupLocalAuthHeader = function() {
    var headerViewModelParams = {
      title: 'Settings',
      startBtn: {
        id: 'backBtn',
        click: this.goBackFromLocalAuthConfig.bind(this),
        display: 'icons',
        label: 'Back',
        icons: 'oj-hybrid-applayout-header-icon-back oj-fwk-icon',
        visible: true
      },
      endBtn: {
        visible: false
      }
    };
    moduleHelper.setupStaticModule(this, 'localAuthHeaderConfig', 'basicHeader', headerViewModelParams);
  };

  AppControllerViewModel.prototype.localLoginCompleted = function(err, authSuccess) {
    if (err && typeof err  === 'object') {
      var reason = 'Log in using credentials. Reason: ' + authErrTrsl.getTranslationForError(err);
      this.appMessages.push({
        severity: 'error',
        summary: 'Local Authentication Failed',
        detail: reason,
        autoTimeout: 0
      });
      this.goToSignIn();
    } else if (authSuccess !== undefined && authSuccess === false) {
      this.goToSignIn();
    }

    this.setPageContentModuleVisibility(true);
  };

  AppControllerViewModel.prototype.onLocalAuthResumeStart = function(event, vm) {
    vm.setPageContentModuleVisibility(false);
  };

  AppControllerViewModel.prototype.onLocalAuthResumeEnd = function(event, vm) {
    vm.localLoginCompleted(null, event.detail.success);
  };

  AppControllerViewModel.prototype.enqueMessage = function(message) {
    this.appMessages.push(message);
  };

  AppControllerViewModel.prototype.onLocalAuthMessage = function(event, vm) {
    vm.enqueMessage(event.detail.message);
  };

  AppControllerViewModel.prototype.appMessageClosed = function(event, vm) {
    vm.appMessages.remove(event.detail.message);
  };

  AppControllerViewModel.prototype.onLoginSuccess = function() {
    this.pushClient.registerForNotifications();
    this.router.go('incidents/incidentsTabDashboard')
    .then(function() {
      this.setPageContentModuleVisibility(true);
    }.bind(this));
  };

  AppControllerViewModel.prototype.signIn = function() {
    if (!this.localFlow) {
      this.goToSignIn();
      return;
    }

    var self = this;
    self.localFlow.getManager().getEnabled()
    .then(function(enabled) {
      if (enabled.length > 0) {
        self.setPageContentModuleVisibility(false);
        return self.localFlow.login();
      }

      return Promise.reject("Local authentication not configured.");
    })
    .then(self.onLoginSuccess.bind(self))
    .catch(self.localLoginCompleted.bind(self));
  };

  AppControllerViewModel.prototype.initLocalAuth = function() {
    var self = this;
    this.pageContentModuleDisplay = ko.observable('none');
    if (!window.cordova || !window.cordova.plugins || !window.cordova.plugins.IdmAuthFlows) {
        self.setPageContentModuleVisibility(true);
      return;
    }

    self.localAuthBuilder = ko.observable(new window.cordova.plugins.IdmAuthFlows.LocalAuthPropertiesBuilder().id("LocalAuthDemo"));
    var cca = document.getElementById("localAuth");
    oj.Context.getContext(cca).getBusyContext().whenReady()
    .then(function(){
      return cca.getFlowPromise();
    })
    .then(function(flow) {
      self.localFlow = flow;
      self.signIn();
    }).catch(self.signIn.bind(self));
  };

  return new AppControllerViewModel();
});
