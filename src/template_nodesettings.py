settings = {
  'controllerName': 'nodeXYZ', # Used for DHCP hostname
  'logInclude': ['.*'], # regex supported
  'logExclude': [], # regex supported
  'debug' : True,
  'httpTimeout': 5, # seconds

  # Auto-Updating
  'gogsRemote': 'http://aaa.bbb.ccc.ddd:pppp/gogs/nodeXYZ',   # URL of mpy prject Repo in the Gogs server
  'gogsBranch': 'master',
  'gogsToken': '1234567890abcdef123456789', # generated in your Gogs user settings
}
