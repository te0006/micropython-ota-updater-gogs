# MicroPython OTA Updater

## Overview

Based off of [Joshua Bellamys fork of rdehuyss's MicroPython OTA Updater](https://github.com/smysnk/micropython-ota-updater). 

Unlike these previous projects (which offer OTA updates from GitHub repositories) this project provides MicroPython OTA updating from a Gogs repository. [Gogs](https://gogs.io , https://github.com/gogs/gogs) is a Git server similar to a subset of GitHub or GitLab, written in golang, and lightweight enough to be deployed on a Raspberry Pi.

Also this variant is focused on nodes which are MQTT clients. 

After boot, a connection to an MQTT broker is attempted. If it fails, the system reboots after a short wait. I. e. the process will only continue once the MQTT broker is accessible.

Then the updater (`update.py`) is called, checks the designated branch for updates and downloads them if HEAD is not current (other release strategies may be added later).

Finally, the node software stored on the pyboard (and possibly just updated OTA) is launched.
However, a watchdog process is launched as well which the node software has to feed regulary.
If it stops to do so (e.g. because the node software has crashed), the watchdog will reset the pyboard, and the process bgins anew.

Thus an OTA update can be triggered for all nodes by stopping the MQTT broker for a short while.

## Hardware compatibility

This software was tested on ESP32 only and will likely not work on ESP8266.

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

Execution of `main.py` calls `updater.update()` checking `.version` file with the SHA of the latest commit.  If they are different it will create a new directory and pull down the `src` sub-directory of that repo.  Once complete, the old `src` directory is deleted and the new copy is moved in its place.  After that it will execute `src.main.start()` with environment settings passed in the "env" argument.

Note: main.py and boot.py in the pyboard's root directory are never overwritten by the OTA update; they remain as they were transferred by `make rsync` .
The OTA updater only installs into the 'src/' folder  of the pyboard.

## Secrets

The files `src/wifisettings.py` and `src/nodesettings.py` are used to store secrets that will be used to configure the pyboard's WiFi, or will be passed to `main.start()`, respectively. These files SHALL NOT be stored in the repository, and so they will not be updated via OTA. Thus they need to be transferred/updated manually by `make rsync` which will put them in the pyboard's root directory, where they won't be affected by OTA updates.
