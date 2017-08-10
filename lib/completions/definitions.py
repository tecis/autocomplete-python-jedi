from utils import top_definition, get_definition_type


def get_definitions(definitions):
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
                definition = top_definition(definition)
            if not definition.module_path:
                continue
            _definition = {
                'text': definition.name,
                'type': get_definition_type(definition),
                'fileName': definition.module_path,
                'line': definition.line - 1,
                'column': definition.column
            }
            _definitions.append(_definition)
    return _definitions
