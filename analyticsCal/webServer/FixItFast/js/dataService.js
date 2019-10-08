/**
 * @license
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
/**
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */

// handles API calls to MCS backend

'use strict';
define(['jquery', 'appConfig'], function ($, appConfig) {

  var baseUrl = appConfig.backendUrl;
  var registrationUrl = appConfig.registrationUrl;

  // Note, the appConfig contains a Basic Authentication header. The use of Basic Auth is
  // not recommended for production apps.
  var baseHeaders = appConfig.backendHeaders;

  var localUrl = 'localData/';

  var useMobileBackend = true;

  function setUseMobileBackend(use) {
    useMobileBackend = use;
  }

  let busyRequest = undefined;
  $(document).ajaxStart(function(event) {
    var done = oj.Context.getPageContext().getBusyContext().addBusyState({
      description: event
    });
    busyRequest = done;
  });
  $(document).ajaxStop(function(event) {
    busyRequest && busyRequest();
    busyRequest = undefined;
  });

  function registerForNotifications(registration) {
    return $.ajax({
      type: 'POST',
      url: registrationUrl,
      headers: baseHeaders,
      data: JSON.stringify(registration),
      contentType: 'application/json; charset=UTF-8'
    });
  }

  function getCustomers() {
    if(useMobileBackend)
      return $.ajax({
        type: 'GET',
        dataType: 'text',
        headers: baseHeaders,
        url: baseUrl + 'customers'
      });
    else {
      return $.ajax(localUrl + 'customers.txt');
    }
  }

  function createCustomer(customer) {
    return $.ajax({
      type: 'POST',
      dataType: 'text',
      headers: baseHeaders,
      data: JSON.stringify(customer),
      url: baseUrl + 'customers',
      contentType: 'application/json; charset=UTF-8'
    });
  }

  function updateCustomer(id, customer) {
    return $.ajax({
      type: 'PATCH',
      headers: baseHeaders,
      data: JSON.stringify(customer),
      url: baseUrl + 'customers/' + id,
      contentType: 'application/json; charset=UTF-8'
    });
  }

  function getCustomer(id) {
    if(id) {
      if(useMobileBackend) {
        return $.ajax({
          type: 'GET',
          dataType: 'text',
          headers: baseHeaders,
          url: baseUrl + 'customers/' + id
        });
      } else {

        var promise = new Promise(function(resolve, reject){
          $.get(localUrl + 'customers.txt').done(function(response) {
            var customers = JSON.parse(response).result;
            var customer = customers.filter(function(customer) { return customer.id === id; });
            resolve(JSON.stringify(customer[0]));
          }).fail(function(response){
            reject(response);
          });
        });

        return promise;
      }
    }

    return $.when(null);
  }

  function getIncidents() {
    if(useMobileBackend)
      return $.ajax({
        type: 'GET',
        dataType: 'text',
        headers: baseHeaders,
        url: baseUrl + 'incidents?technician=~'
      });
    else {
      return $.get(localUrl + 'incidents.txt');
    }
  }

  function getIncidentsStats() {
    if(useMobileBackend)
      return $.ajax({
        type: 'GET',
        dataType: 'text',
        headers: baseHeaders,
        url: baseUrl + 'stats/incidents?technician=~'
      });
    else {
      return $.get(localUrl + 'incidentsStats.txt');
    }
  }

  function getIncidentsHistoryStats() {
    if(useMobileBackend) {
      return $.ajax({
        type: 'GET',
        dataType: 'text',
        headers: baseHeaders,
        url: baseUrl + 'stats?technician=~&period=annual'
      });
    } else {
      return $.get(localUrl + 'incidentsHistoryStats.txt');
    }
  }

  function createIncident(incident) {
    return $.ajax({
      type: 'POST',
      headers: baseHeaders,
      url: baseUrl + 'incidents',
      contentType: 'application/json; charset=UTF-8',
      data: JSON.stringify(incident)
    });
  }

  function getIncident(id) {
    if(id)
      if(useMobileBackend) {
        return $.ajax({
          type: 'GET',
          dataType: 'text',
          headers: baseHeaders,
          url: baseUrl + 'incidents/' + id
        });
      } else {
        return $.get(localUrl + 'incidents/' + id + '.txt');
      }

    return $.when(null);
  }

  function updateIncident(id, incident) {
    if(id)
      return $.ajax({
        type: 'PUT',
        headers: baseHeaders,
        url: baseUrl + 'incidents/' + id,
        contentType: 'application/json; charset=UTF-8',
        data: JSON.stringify(incident)
      });
    return $.when(null);
  }

  function getIncidentActivities(id) {
    if(id) {
      if(useMobileBackend) {
        return Promise.resolve($.ajax({
          type: 'GET',
          dataType: 'text',
          headers: baseHeaders,
          url: baseUrl + 'incidents/' + id + '/activities'
        }));
      } else {
        return $.get(localUrl + 'incidents/' + id + '/activities.txt');
      }
    }
  }

  function postIncidentActivity(id, comment, picture) {
    if(id && comment) {

      var activity = { comment: comment, picture: picture };

      return $.ajax({
        type: 'POST',
        dataType: 'text',
        headers: baseHeaders,
        url: baseUrl + 'incidents/' + id + '/activities',
        contentType: 'application/json; charset=UTF-8',
        data: JSON.stringify(activity)
      });
    } else {
      return $.when(null);
    }
  }

  function updateIncidentActivity(id, actid, content) {
    if(id && actid && content)
      return $.ajax({
        type: 'PATCH',
        headers: baseHeaders,
        url: baseUrl + 'incidents/' + id + '/activities/' + actid,
        data: JSON.stringify(content),
        contentType: 'application/json; charset=UTF-8'
      });
    else
      return $.when(null);
  }

  function getLocation(id) {
    if(id) {
      if(useMobileBackend) {
        return $.ajax({
          type: 'GET',
          dataType: 'text',
          headers: baseHeaders,
          url: baseUrl + 'locations/' + id
        });
      } else {

        var promise = new Promise(function(resolve, reject){
          $.get(localUrl + 'locations.txt').done(function(response) {
            var locations = JSON.parse(response);
            var location = locations.filter(function(location) { return location.id === id; });
            resolve(JSON.stringify(location[0]));
          }).fail(function(response){
            reject(response);
          });
        });

        return promise;
      }

    } else {
      return $.when(null);
    }

  }

  function getUserProfile() {
    if(useMobileBackend)
      return $.ajax({
        type: 'GET',
        dataType: 'text',
        headers: baseHeaders,
        url: baseUrl + 'users/~'
      });
    else {
      return $.get(localUrl + 'users.txt');
    }
  }

  function updateUserProfile(user) {
    return $.ajax({
      type: 'PATCH',
      headers: baseHeaders,
      url: baseUrl + 'users/~',
      contentType: 'application/json; charset=UTF-8',
      data: JSON.stringify(user)
    });
  }

  return {
    registerForNotifications: registerForNotifications,
    getCustomers: getCustomers,
    createCustomer: createCustomer,
    updateCustomer: updateCustomer,
    getCustomer: getCustomer,
    getIncidents: getIncidents,
    getIncidentsStats: getIncidentsStats,
    getIncidentsHistoryStats: getIncidentsHistoryStats,
    createIncident: createIncident,
    getIncident: getIncident,
    updateIncident: updateIncident,
    getIncidentActivities: getIncidentActivities,
    postIncidentActivity: postIncidentActivity,
    updateIncidentActivity: updateIncidentActivity,
    getLocation: getLocation,
    getUserProfile: getUserProfile,
    updateUserProfile: updateUserProfile,
    setUseMobileBackend: setUseMobileBackend
  };

});
