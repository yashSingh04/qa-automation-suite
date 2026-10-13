# Test applications

The mobile suite runs against **ApiDemos**, the Android sample app that
Appium uses for its own test suite. It is not committed here (APKs do not
belong in git); download it once:

```bash
curl -L -o apps/ApiDemos-debug.apk \
  https://github.com/appium/android-apidemos/releases/download/v3.1.0/ApiDemos-debug.apk
```

CI downloads it automatically in the `mobile-tests` job.

If the APK is absent, the Appium fixture falls back to launching the app by
package and activity, which works when it is already installed on the device.
