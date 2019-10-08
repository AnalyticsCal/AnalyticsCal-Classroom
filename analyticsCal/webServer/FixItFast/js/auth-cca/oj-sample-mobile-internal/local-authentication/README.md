# local-authentication component

[cordova-plugin-oracle-idm-auth](https://github.com/oracle/cordova-plugin-oracle-idm-auth)
plugin supports local authentication types such as passcode and fingerprint.
There are use cases such as setting up a passcode, changing a passcode, authenticating using passcode
which needs UI. UI is also needed for configuring passcode and fingerprint based authentications.

This component provides out of the box UI for these purposes.

Note: This component is only for mobile and
needs [cordova-plugin-oracle-idm-auth](https://github.com/oracle/cordova-plugin-oracle-idm-auth) plugin to be installed.

## Usage

Add the component to your page as follows

```html
<oj-sample-mobile-internal-local-authentication id="localAuth" builder="[[localAuthBuilder]]"
                      show-dismiss-button="true"
                      on-oj-dismissed="[[onDismissed]]"
                      app-name="App"
                      company-name="Company"
                      min-passcode-length="5"
                      max-passcode-length="8"
                      enable-resume-challenge="true">
</oj-sample-mobile-internal-local-authentication>
```

The builder passed to the component should be one created using the [plugin's](https://github.com/oracle/cordova-plugin-oracle-idm-auth)
[local authentication builder](https://oracle.github.io/cordova-plugin-oracle-idm-auth/LocalAuthPropertiesBuilder.html).
The component will set its own passcode challenge handler on the builder. So any challenge handler already set will be overwritten.

The JS code should look something like this

```js
  // Builder object bound to the component
  self.localAuthBuilder = new idmAuthFlows.LocalAuthPropertiesBuilder()
                            .id("myLocalAuth");

  // Obtain the flow promise from the component and wait for it to resolve.
  // When resolved this promise will return the auth flow.
  // App should hold on to this instance for doing authentication tasks.
  var flowPromise = document.getElementById("myBasicAuth").getFlowPromise();
  flowPromise
    .then(function(flow) {
      // Preserve the flow for future interactions.
      self.localAuthFlow = flow;
      return flow.login();
    })
    .then(function() {
      // Handle login success.
    })
    .catch(function(err) {
      // Handle error
    });

  // Bind this to dismissed event
  self.onDismissed = function() {
    // Restore the app page to be shown to the user
  }
```
