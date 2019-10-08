ADDITIONAL INSTALLATION INFORMATION
-----------------------------------

Having scaffolded a web app using this template zip, follow these instructions to build and serve the app.

1. Theming - the app requires a custom theme
  a. Install node-sass:
    ojet add sass
  b. Build app with existing custom theme:
    ojet build --theme=fif:android
  c. Serve app with existing custom theme:
    ojet serve --theme=fif:android

  * Note: FIF uses the css it needs by enabling specific $include* variables in its sass files. To enable theming for other components, toggle $include* vars in FIF scss as needed. See JET SASS variable documentation for more details.
2. Hybrid App Configuration
  a. Extend to hybrid project:
    ojet add hybrid --platforms=android,ios,windows --appid=com.jet.fixitfast --appname=FixItFast

    * If you intend to deploy to an iOS device, specify an appid that matches your iOS provisioning profile
    * If you have already scaffolded the app and wish to change the appid, you can edit hybrid/config.xml
    * You can only deploy to iOS from a Mac and you can only deploy to Windows from Windows 10

  b. Install Cordova plugins:
    ojet add plugins cordova-plugin-camera cordova-plugin-contacts cordova-plugin-geolocation cordova-plugin-splashscreen cordova-plugin-network-information cordova-plugin-wkwebview-file-xhr cordova-plugin-file cordova-plugin-device cordova-plugin-keyboard cordova-plugin-statusbar cordova-plugin-oracle-idm-auth

    * The following plugin versions have been tested with Cordova CLI v8.0.0:
      cordova-plugin-file@6.0.1
      cordova-plugin-camera@2.4.1
      cordova-plugin-contacts@2.3.1
      cordova-plugin-geolocation@2.4.3
      cordova-plugin-splashscreen@4.0.3
      cordova-plugin-network-information@1.3.3
      cordova-plugin-wkwebview-file-xhr@2.1.1
      cordova-plugin-device@2.0.2
      cordova-plugin-keyboard@1.2.0
      cordova-plugin-statusbar@2.4.2
      cordova-plugin-oracle-idm-auth@1.1.3

  c. Add the following configurations to hybrid/config.xml
     Within <platform name="android”>:
       <preference name="ShowSplashScreenSpinner" value="false" />
       <preference name="FadeSplashScreen" value="false" />
       <preference name="AutoHideSplashScreen" value="false" />
     Within <platform name="ios”>:
       <allow-intent href="maps:*" />
       <preference name="SplashScreenDelay" value="2000" />
       <preference name="ShowSplashScreenSpinner" value="false" />
       <preference name="FadeSplashScreen" value="true" />
       <preference name="AutoHideSplashScreen" value="true" />
       <preference name="KeyboardShrinksView" value="true" />
       <edit-config file="*-Info.plist" mode="merge" target="NSCameraUsageDescription">
           <string>Take photo for avatar or incident report</string>
       </edit-config>
       <edit-config file="*-Info.plist" mode="merge" target="NSPhotoLibraryUsageDescription">
           <string>Retrieve image from photo library for avatar or incident report</string>
       </edit-config>
       <edit-config file="*-Info.plist" mode="merge" target="NSLocationWhenInUseUsageDescription">
           <string>Access location information to tag photos</string>
       </edit-config>
       <edit-config file="*-Info.plist" mode="merge" target="NSPhotoLibraryAddUsageDescription">
           <string>Add photo to photo library</string>
       </edit-config>
       <edit-config file="*-Info.plist" mode="merge" target="NSContactsUsageDescription">
           <string>Add customer to contacts</string>
       </edit-config>

    * Depending on your cordova-ios version, you may need to remove and re-add the ios platform to your app:
      ojet remove platform ios; ojet add platform ios

  d. If you wish to use Google maps rather than Oracle maps, follow the instructions in incidentsTabMap.js and incidentTabMap.js

3. Enable a full-access backend (optional)
    * By default, the app has read-only access to a public instance of an Oracle Mobile Hub mobile backend (MBE)
    * The app supports full read-write access, which can be enabled as follows:
  a. Implement your own MBE that provides PUT, POST, PATCH and DELETE APIs in addition to the GET APIs required by the client app
  b. Enable create & update features in the app by setting self.isReadOnlyMode = false; in src/js/appController.js
  c. Edit src/js/appConfigExternal.js to specify the connection details of the MBE you have implemented in step a

4. Enable push notifications (optional)
    * The app supports push notifications, which can be enabled as follows:
  a. Follow all the steps 3a-3c above
  b. Create a Google Project that uses Firebase Cloud Messaging and/or create an iOS provisioning profile with push capability
  c. Add Android & iOS mobile clients to your MBE and in their profiles specify the requisite FCM & APNs details obtained in step b
  d. In your MBE, call the Oracle Mobile Hub API to initiate a push notification to registered devices when an incident is created
  e. Edit src/js/appConfigExternal.js to specify the Google Project ID obtained in step b as the 'senderID' for your MBE
  f. Edit src/js/PushClient.js to uncomment lines 100-104
  g. Add the phonegap-plugin-push Cordova plugin to the app and specify the Google Project ID obtained in step b as the SENDER_ID
  h. If you install v2 of phonegap-plugin-push, you will be required to add the google-service.json file to your Android project and you will be required to install Cocoapods for iOS.
     Refer to the plugin's online documentation for details.  To avoid this, you can install the latest v1 of the plugin instead.
  i. On iOS, build the app using the push-enabled provisioning profile you created in step b

  * Both versions 1.10.5 and 2.0.0 of the phonegap-plugin-push plugin have been tested with Cordova CLI v7.0.1

5. Build and serve the app
  a. To serve web app with fif android theme
    ojet serve web --theme=fif:android
  b. To serve hybrid app with fif theme to iOS simulator
    ojet serve ios --theme=fif
  b. To serve hybrid app with fif theme to Android device
    ojet serve android --theme=fif --device
  c. To serve hybrid app with fif windows theme to browser
    ojet serve windows --theme=fif --browser

    * To deploy to an iOS device or to deploy in release mode to Android, you will require a buildConfig.xml file that specifies
      your signing credentials.  For more information about this, refer to the JET Developer Guide.

6. Enable and debug service worker (optional)
  a. Enable service worker
    * When running as a web app on browsers that support service worker, the app supports push notification and caching static files offline.
    * Service worker is disabled by default. To enable it, uncomment the service worker code block in index.html.
      /* START: service worker code */
      [code]
      /* END: service worker code */
  b. Debug service worker
    * When the app is served locally and you are working on javascript or css changes, you should force the service worker to always fetch files served from the local server. Otherwise the service worker will load cached js/css and you won’t see your changes. This can be enabled by checking ‘Bypass for network’ in Chrome dev tools > Application tab > Service worker > Bypass for network.
    * To unregister a service worker in Chrome, visit chrome://serviceworker-internals
    * When you are working on the service worker code, you should force the service worker to update on reload. This can be enabled by checking ‘Update on reload’ in Chrome dev tools > Application tab > Service worker > Update on reload.
