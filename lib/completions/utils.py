basic_types = {
    'module': 'import',
    'instance': 'variable',
    'statement': 'value',
    'param': 'variable',
}


def get_definition_type(definition):
    is_built_in = definition.in_builtin_module
    if definition.type not in ['import', 'keyword'] and is_built_in():
        return 'builtin'
    if definition.type in ['statement'] and definition.name.isupper():
        return 'constant'
    return basic_types.get(definition.type, definition.type)


def top_definition(definition):
    for d in definition.goto_assignments():
        if d == definition:
            continue
        if d.type == 'import':
            return _top_definition(d)
        else:
            return d
    return definition


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


def generate_signature(completion):
    """Generate signature with function arguments.
    """
    if completion.type in ['module'] or not hasattr(completion, 'params'):
        return ''
    return '%s(%s)' % (
        completion.name,
        ', '.join(p.description for p in completion.params if p))


def additional_info(completion):
    """Provide additional information about the completion object."""
    if completion._definition is None:  # TODO v0.10.2 issue
        return ''
    if completion.type == 'statement':
        nodes_to_display = ['InstanceElement', 'String', 'Node', 'Lambda',
                            'Number']
        return ''.join(c.get_code() for c in
                       completion._definition.children if type(c).__name__
                       in nodes_to_display).replace('\n', '')
    return ''
