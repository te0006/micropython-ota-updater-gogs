# MicroPython OTA Updater

## Overview

Based off of [rdehuyss's MicroPython OTA Updater](https://github.com/rdehuyss/micropython-ota-updater). This MicroPython Over-The-Air Updater will follow a GitHub branch, checking for updates on boot.  Will update if HEAD is not current (other release strategies may be added later).

> Note: due to a bug in the SSL library of ESP8266 devices, micropython-ota-updater cannot be used on these devices. See https://github.com/rdehuyss/micropython-ota-updater/issues/6 and https://github.com/micropython/micropython/issues/6737

## Gettings started

Edit `src/env.py` to fill in WiFi credentials, GitHub remote repository / branch and optional GitHub credentials to increase API limits.

The `src/main.py` will call `updater.update()` which will pull down remote to the `src` directory.  After that it will execute `src.main` with the following kargs:
```
import src.main
src.main.start(env=env, requests=lib.requests, logger=logger, time=t, updater=updater)
```

For example implementation check out the [my-grow project](https://github.com/smysnk/my-grow).

## Deployment

`make install` # Install local Python dependencies (rshell & esptool)

`make erase` # Erase ESP32

`make image` # Install MicroPython on ESP32

`make rsync` # Install `updater` on ESP32

`make repl` # Opens a repl terminal to the ESP32

Power cycle the ESP32, you should see the updater pull down HEAD of the configured branch on boot.

## Secrets

Use `src/env.py` to store secrets that will be passed to `main.start()` so they do not need be stored in the main repository.

## Interval Updating

You may want to check for updates a regularly scheduled intervals eg. every hour. Here is an [example implementation](https://github.com/smysnk/my-grow/blob/master/src/sensorloop.py#L216):
```
# Reset the device if an update is available
if state['runtime'][runtime.OTA_AUTO_UPDATE_INTERVAL] and time.time() % state['runtime'][runtime.OTA_AUTO_UPDATE_INTERVAL] == 0:
  try:
    gc.collect()
    updater.checkForUpdate()
  except Exception as e:
    log('Failed to check for OTA update:', e)
```