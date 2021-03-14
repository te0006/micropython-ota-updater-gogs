import network, ntptime, machine, wifisettings, nodesettings, time
import lib.timew

sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
  print('Connecting to network...')
  sta_if.active(True)
  sta_if.config(dhcp_hostname=nodesettings.settings['controllerName'])
  sta_if.connect(wifisettings.settings['wifiAP'], wifisettings.settings['wifiPassword'])
  while not sta_if.isconnected():
    pass

  # Get current time from internets
  ntptime.settime()
