import update, env, lib.requests, lib.logger, lib.requests, lib.timew, time, os, machine

t = lib.timew.Time(time=time)

# Configure Logger
logger = lib.logger.config(enabled=env.settings['debug'], include=env.settings['logInclude'], exclude=env.settings['logExclude'], time=t)
log = logger(append='boot')
log("The current time is %s" % t.human())

loggerOta = logger(append='OTAUpdater')

io = update.IO(os=os, logger=loggerOta)
gogs = update.Gogs(
  remote=env.settings['gogsRemote'],
  branch=env.settings['gogsBranch'],
  token=env.settings['gogsToken'],
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
src.main.start(env=env, requests=lib.requests, logger=logger, time=t, updater=updater)
