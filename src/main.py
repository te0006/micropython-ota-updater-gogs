import time, machine, update, wifisettings, nodesettings, lib.requests, lib.logger, lib.requests, lib.timew, time, os, machine
from umqtt.robust import MQTTClient
from machine import Pin, WDT
led = Pin(2, Pin.OUT)
led.off()

t = lib.timew.Time(time=time)

# Configure Logger
logger = lib.logger.config(enabled=nodesettings.settings['debug'], include=nodesettings.settings['logInclude'], exclude=nodesettings.settings['logExclude'], time=t)
log = logger(append='boot')
log("The current time is %s" % t.human())

mqtt_pth = nodesettings.settings['controllerName']
client = MQTTClient(mqtt_pth, 
wifisettings.settings['mqtt_ip'], 
port=wifisettings.settings['mqtt_port'])

mq_c = False
for i in range(1):
  try:
    client.connect()
    mq_c = True
  except:
    log('MQTT: cannot connect')
    led.on()
    time.sleep(1)
if not mq_c:
  log ('MQTT: giving up, resetting')
  time.sleep(1)
  machine.reset()
log('MQTT: connected OK')
led.off()

def mqtt_pub(tag, data):
    client.publish(mqtt_pth+"/"+tag, 
    data)

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
  log('OTA update OK')
  mqtt_pub("boot", "OTA_OK")
  led.off()
except Exception as e:
  log('Failed to OTA update:', e)
  mqtt_pub("boot", "OTA_error")
  led.on()


env = {}
env.update(nodesettings.settings)
env['requests'] = lib.requests
env['log'] = logger(append='main')
env['time'] = t
env['updater'] = updater

env['wdt'] = WDT(timeout=5000) # watchdog timer. If feed() is not called every 5000ms (max) the system will reset.
    # the main loop (within src.main.start) calls feed() periodically but will stop doing so in case of an exception
    # If communication to the MQTT broker fails, an exception will occur.
    # Thus, the system can be remote-reset by stopping the MQTT broker.
    # Due to measures in micropython-ota-updater-gogs/src/main.py, the system will then boot-loop 
    # until the MQTT server is accesible again, and then check for an OTA update.
    # In summary, after an update of the node code has been published on Gogs, nodes can be forced to load it 
    # by stopping the MQTT broker service for a short while. 


env['mqtt_pub'] = mqtt_pub
env['wdt'].feed()

log('launching src.main.start()')
import src.main
src.main.start(env)
