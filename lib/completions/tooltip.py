from utils import  top_definition, additional_info, get_definition_type


def get_tooltip(definitions):
    _definitions = []
    for definition in definitions:
        if definition.module_path:
            if definition.type == 'import':
                definition = top_definition(definition)
            if not definition.module_path:
                continue

            description = definition.docstring()
            if description is not None:
                description = description.strip()
            if not description:
                description = additional_info(definition)
            _definition = {
                'text': definition.name,
                'type': _get_definition_type(definition),
                'fileName': definition.module_path,
                'description': description,
                'line': definition.line - 1,
                'column': definition.column
            }
            _definitions.append(_definition)
            break
    return _definitions
