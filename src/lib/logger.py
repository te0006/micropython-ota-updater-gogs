import re
import io

def config(time=None, enabled=False, include=None, exclude=None):
  logger = Logger(time=time, enabled=enabled, include=include, exclude=exclude)

  def log(*args, append=None, existing='', name=''):
    if append:
      existing = existing + ':' + append
      return lambda *args, append=None, name='': log(*args, name=name, append=append, existing=existing)
    
    name = (existing + ':' + name).lstrip(':').rstrip(':')
    return logger(*args, name=name)
    
  return log

class Logger:
  def __init__(self, time=None, enabled=False, include=None, exclude=None):
    self.print = print
    self.time = time
    self.enabled = enabled
    self.include = list(map(re.compile, include))
    self.exclude = list(map(re.compile, exclude))

  def __call__(self, *args, name=''):
    if not self.enabled:
      return

    included = False
    excluded = False
    for include in self.include:
      if include.search(name):
        included = True
    for exclude in self.exclude:
      if exclude.search(name):
        excluded = True

    if not included and not excluded:
      return
    elif not included and excluded:
      return
    elif included and not excluded:
      pass
    elif included and excluded:
      return

    statement = []
    for arg in args:
      statement.append('%s' % arg)
    
    statement = "[%s][%s] %s" % (self.time.dateTimeIso(), name, ' '.join(statement))
    self.print(statement)
    return statement

