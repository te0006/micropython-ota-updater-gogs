import update, wifisettings, nodesettings, lib.requests, lib.logger, lib.requests, lib.timew, time, os, machine

t = lib.timew.Time(time=time)

# Configure Logger
logger = lib.logger.config(enabled=nodesettings.settings['debug'], include=nodesettings.settings['logInclude'], exclude=nodesettings.settings['logExclude'], time=t)
log = logger(append='boot')
log("The current time is %s" % t.human())

loggerOta = logger(append='OTAUpdater')

io = update.IO(os=os, logger=loggerOta)
gogs = update.Gogs(
  remote=nodesettings.settings['gogsRemote'],
  branch=nodesettings.settings['gogsBranch'],
  token=nodesettings.settings['gogsToken'],
  requests = lib.requests,
  io=io,
  logger=loggerOta,
)
updater = update.OTAUpdater(io=io, gogs=gogs, logger=loggerOta, machine=machine)

try:
  updater.update()
except Exception as e:
  log('Failed to OTA update:', e)

import src.main
src.main.start(env=nodesettings, requests=lib.requests, logger=logger, time=t, updater=updater)
