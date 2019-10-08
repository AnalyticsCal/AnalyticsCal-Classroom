/**
 * @license
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
/**
  Copyright (c) 2015, 2018, Oracle and/or its affiliates.
  The Universal Permissive License (UPL), Version 1.0
*/
'use strict';
define(['ojL10n!./resources/nls/auth-error-translations-strings'],
  function (translations) {
    function ErrorTranslationsModel() {
      this.translations = translations;
    }

    /**
     * Method to convert error object to translated error message.
     * @param {object} error 
     */
    ErrorTranslationsModel.prototype.getTranslationForError = function(error) {
      if (error.errorSource === 'system')
        return error.translatedErrorMessage;

      var message = this.translations.errorMessages[error.errorCode];
      if (!message)
        return this.translations.errorMessages.unknownErrorCode + error.errorCode;
      return message;
    };

    return new ErrorTranslationsModel();
  }
);