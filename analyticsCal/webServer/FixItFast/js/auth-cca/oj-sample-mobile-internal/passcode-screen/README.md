# passcode-screen component

This is a component which provides UI for capturing passcode from user.

## Usage

Add the component to your page as follows

```html
<oj-sample-mobile-internal-passcode-screen id="passcodeScreen"
                 on-oj-done="[[done]]"
                 validate-passcode-length="true"
                 company-name="myCompany"
                 app-name="myApp"
                 go-text="Yo!"></oj-sample-mobile-internal-passcode-screen>
```

The JS code should look something like this

```js
self.done = function() {
  var passcodeFromUser = document.getElementById("passcodeScreen").getPasscode();
  // Do something useful with passcode.
};
```

Custom error messages can be set using

```js
document.getElementById("passcodeScreen").setError('Custom error message');
```

Passcode held by the component can be cleared using

```js
document.getElementById("passcodeScreen").clearPasscode();
```