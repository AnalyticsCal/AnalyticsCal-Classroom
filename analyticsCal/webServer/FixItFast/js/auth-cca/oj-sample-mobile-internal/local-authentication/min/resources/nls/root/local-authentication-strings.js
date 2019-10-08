/**
 * @license
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
/**
  Copyright (c) 2015, 2018, Oracle and/or its affiliates.
  The Universal Permissive License (UPL), Version 1.0
*/
define({
  "ojSampleMobileLocalAuthentication": {
    "initError":"Error while initializing flow",
    "authError":"Local Authentication Failed",
    "configError":"Error while configuring local authentication",
    "passcodeChallenge" : {
      "enterCurrPasscodeMsg":"Enter Passcode",
      "enterNewPasscodeMsg":"Enter New Passcode",
      "reEnterNewPasscodeMsg":"Re Enter New Passcode",
      "passcodeMismatch": "Passcodes provided did not match."
    },
    "configure" : {
      "enablePasscode":"Passcode",
      "changePasscode":"Change Passcode",
      "enableFingerprint":"Fingerprint",
      "done":"Done",
      "errorHeader":"Error",
      "fingerprintMessageHeader":"Fingerprint availability status",
      "fingerprintAvailableNotEnrolled":"Fingerprint support is available on device but not enrolled. Fix this to enable fingerprint for this app.",
      "fingerprintLocked": "Fingerprint enrolled on the device is locked out due to max retrys. Fix this to enable fingerprint for this app.",
      "fingerprintUnavailable": "Fingerprint support is not available on this device."
    },
    "fingerprint": {
      "promptMessage": "User fingerprint to unlock content",
      "pinFallbackButtonLabel": "Enter Passcode",
      "cancelButtonLabel": "Cancel",
      "hintText": "Scan your finger",
      "promptTitle": "Unlock with Fingerpint",
      "successMessage": "Authentication successful.",
      "errorMessage": "Authentication failed."
    }
  }
});
