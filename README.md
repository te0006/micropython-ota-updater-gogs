# MicroPython OTA Updater

## Overview

Based off of [Joshua Bellamys fork of rdehuyss's MicroPython OTA Updater](https://github.com/smysnk/micropython-ota-updater). This MicroPython Over-The-Air Updater will follow a Gogs (https://gogs.io , or self-hosted using https://github.com/gogs/gogs) branch, checking for updates on boot.  Will update if HEAD is not current (other release strategies may be added later).

> Note: due to a bug in the SSL library of ESP8266 devices, micropython-ota-updater cannot be used on these devices. See https://github.com/rdehuyss/micropython-ota-updater/issues/6 and https://github.com/micropython/micropython/issues/6737

## Getting started

Edit `src/env.py` to fill in WiFi credentials, Gogs remote repository, branch , and an access token generated in Gogs' user management.  Deploy!

For an example implementation check out the [???] project.

## Deployment

`make install` # Install local Python dependencies (rshell & esptool)

`make erase` # Erase ESP32

`make image` # Install MicroPython on ESP32

`make rsync` # Install `updater` on ESP32

`make repl` # Opens a repl terminal to the ESP32

Power cycle (Ctrl-D) the ESP32, you should see the updater pull down HEAD of the configured branch on boot.

## Internals

Execution of `src/main.py` calls `updater.update()` checking `.version` file with the SHA of the latest commit.  If they are different it will create a new directory and pull down the `src` sub-directory.  Once complete, the old `src` directory is deleted and the new copy is moved in its place.  After that it will execute `src.main` with the following kargs:
```
import src.main
src.main.start(env=env, requests=lib.requests, logger=logger, time=t, updater=updater)
```

## Secrets

Use `src/env.py` to store secrets that will be passed to `main.start()` so they do not need be stored in the main repository.  This file is not updated via OTA and needs to be replaced manually by flashing.

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

