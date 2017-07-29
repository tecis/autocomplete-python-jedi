def get_call_signatures(script):
    """Extract call signatures from jedi.api.Script object in failsafe way.

    Returns:
        Tuple with original signature object, name and value.
    """
    _signatures = []
    try:
        call_signatures = script.call_signatures()
    except KeyError:
        call_signatures = []
    for signature in call_signatures:
        for pos, param in enumerate(signature.params):
            if not param.name:
                continue
            if param.name == 'self' and pos == 0:
                continue
            if WORD_RE.match(param.name) is None:
                continue
            try:
                name, value = param.description.split('=')
            except ValueError:
                name = param.description
                value = None
            if name.startswith('*'):
                continue
            _signatures.append((signature, name, value))
    return _signatures


def get_arguments(script):
    """Serialize response to be read from Atom.

    Args:
        script: Instance of jedi.api.Script object.
        identifier: Unique completion identifier to pass back to Atom.

    Returns:
        Serialized string to send to Atom.
    """
    seen = set()
    arguments = []
    i = 1
    for _, name, value in get_call_signatures(script):
        if not value:
            arg = '${%s:%s}' % (i, name)
        elif self.use_snippets == 'all':
            arg = '%s=${%s:%s}' % (name, i, value)
        else:
            continue
        if name not in seen:
            seen.add(name)
            arguments.append(arg)
        i += 1
    snippet = '%s$0' % ', '.join(arguments)
    return snippet
