# Shared Resources

One of the main pain points of [cordova-plugin-oracle-idm-auth](https://github.com/oracle/cordova-plugin-oracle-idm-auth)
plugin users is that the app has to track and translate the errors from the plugin.

This is a shared component for translating [error objects](https://oracle.github.io/cordova-plugin-oracle-idm-auth/global.html#AuthError)
in the plugin to error messages that can be presented to the user.

## Usage

In the JS code, require the  use the following to get the message for an error

```js
define([..., 'oj-sample-mobile-internal/common/auth-error-translations', ...], function(..., translations, ...){
  translations.getTranslationForError(err)
})
```

Error object passed should be of [this type](https://oracle.github.io/cordova-plugin-oracle-idm-auth/global.html#AuthError)