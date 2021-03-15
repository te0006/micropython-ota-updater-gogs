# MicroPython OTA Updater

## Overview

Based off of [Joshua Bellamys fork of rdehuyss's MicroPython OTA Updater](https://github.com/smysnk/micropython-ota-updater). 

Unlike these previous projects (which offer OTA updates from GitHub repositories) this project provides MicroPython OTA updating from a Gogs repository. [Gogs](https://gogs.io , https://github.com/gogs/gogs) is a Git server similar to a subset of GitHub or GitLab, written in golang, and lightweight enough to be deployed on a Raspberry Pi.

During boot, the updater (`update.py`) is called from main.py, checks the designated branch for updates and downloads them if HEAD is not current (other release strategies may be added later).

> Note: due to a bug in the SSL library of ESP8266 devices, micropython-ota-updater cannot be used on these devices. See https://github.com/rdehuyss/micropython-ota-updater/issues/6 and https://github.com/micropython/micropython/issues/6737

## Getting started

Create `src/wifisettings.py` by editing `src_wifisettings.py.template` and filling in WiFi credentials and DNS name of the pyboard.

Create `src/nodesettings.py` by editing `src_nodesettings.py.template` and editing Gogs remote repository, branch , and a Gogs access token generated in Gogs' user management.  

Deploy!

For an example implementation check out the [???] project.

## Deployment

`make install` # Install local Python dependencies (rshell & esptool)

`make erase` # Erase ESP32

`make image` # Install MicroPython on ESP32

`make rsync` # Install `updater` (contents of 'src' folder of this repo) to pyboard (root folder)

`make repl` # Opens a repl terminal to the ESP32

Power cycle (Ctrl-D) the ESP32, you should see the updater pull down HEAD of the configured branch on boot.

## Internals

Execution of `main.py` calls `updater.update()` checking `.version` file with the SHA of the latest commit.  If they are different it will create a new directory and pull down the `src` sub-directory of that repo.  Once complete, the old `src` directory is deleted and the new copy is moved in its place.  After that it will execute `src.main` with the following kargs:
```
import src.main
src.main.start(env=env, requests=lib.requests, logger=logger, time=t, updater=updater)
```

Note: main.py and boot.py in the pyboard's root directory are never overwritten by the OTA update; they remain as they were transferred by `make rsync` .
The OTA updater only installs into the 'src/' folder  of the pyboard.

## Secrets

The files `src/wifisettings.py` and `src/nodesettings.py` are used to store secrets that will be used to configure the pyboard's WiFi, or will be passed to `main.start()`, respectively. These files SHALL NOT be stored in the repository, and so they will not be updated via OTA. Thus they need to be transferred/updated manually by `make rsync` which will put them in the pyboard's root directory, where they won't be affected by OTA updates.

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

