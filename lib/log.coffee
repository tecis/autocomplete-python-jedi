module.exports =
  prefix: 'autocomplete-python-jedi:'
  debug: (msg...) ->
    if atom.config.get('autocomplete-python-jedi.outputDebug')
      return console.debug @prefix, msg...

  warning: (msg...) ->
    return console.warn @prefix, msg...
