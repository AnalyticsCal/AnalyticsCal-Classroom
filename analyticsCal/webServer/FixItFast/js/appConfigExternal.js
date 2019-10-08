/**
 * @license
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
/**
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */

// app configuration for public release

define([], function () {
  return {
    appId: 'com.jet.FixItFast',
    appVersion: '3.0',
    // ReadOnly MBE
    backendName: 'fixitfastclient',
    backendUrl: 'https://6283B441D98B4DB7BD0A83697AF77A37.mobile.ocp.oraclecloud.com:443/mobile/custom/fixitfastclient/',
    backendHeaders: {
      'Oracle-Mobile-Backend-Id': '20462778-ccc4-42df-ac51-7aadaf67258b',
      'Authorization': 'Basic NjI4M0I0NDFEOThCNERCN0JEMEE4MzY5N0FGNzdBMzdfTW9iaWxlQW5vbnltb3VzX0FQUElEOmRiN2RhMmQ3LWVmN2QtNGE0Ny05ODY4LTYwMzdmNGViYzQxOA=='
    },
    registrationUrl: 'https://6283B441D98B4DB7BD0A83697AF77A37.mobile.ocp.oraclecloud.com:443/mobile/platform/devices/register',
    senderID: 'XXXXXXX' // Where the XXXXXXX maps to the project number in the Google Developer Console.
  }
})
