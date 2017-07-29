basic_types = {
    'module': 'import',
    'instance': 'variable',
    'statement': 'value',
    'param': 'variable',
}


def _get_definition_type(definition):
    is_built_in = definition.in_builtin_module
    if definition.type not in ['import', 'keyword'] and is_built_in():
        return 'builtin'
    if definition.type in ['statement'] and definition.name.isupper():
        return 'constant'
    return basic_types.get(definition.type, definition.type)


def _top_definition(self, definition):
    for d in definition.goto_assignments():
        if d == definition:
            continue
        if d.type == 'import':
            return self._top_definition(d)
        else:
            return d
    return definition


def get_definitions(self, definitions, identifier=None):
    """Serialize response to be read from Atom.

    Args:
        definitions: List of jedi.api.classes.Definition objects.
        identifier: Unique completion identifier to pass back to Atom.

    Returns:
        Serialized string to send to Atom.
    """
    _definitions = []
    for definition in definitions:
        if definition.module_path:
            if definition.type == 'import':
                definition = self._top_definition(definition)
            if not definition.module_path:
                continue
            _definition = {
                'text': definition.name,
                'type': self._get_definition_type(definition),
                'fileName': definition.module_path,
                'line': definition.line - 1,
                'column': definition.column
            }
            _definitions.append(_definition)
    return json.dumps({'id': identifier, 'results': _definitions})
