
def get_methods(script):
    _methods = []
    try:
        completions = script.completions()
    except KeyError:
        return []

    for completion in completions:
        if completion.name == '__autocomplete_python':
            instance = completion.parent().name
            break
    else:
        instance = 'self.__class__'

    for completion in completions:
        params = []
        if hasattr(completion, 'params'):
            params = [p.description for p in completion.params if ARGUMENT_RE.match(p.description)]
        if completion.parent().type == 'class':
            _methods.append({
                'parent': completion.parent().name,
                'instance': instance,
                'name': completion.name,
                'params': params,
                'moduleName': completion.module_name,
                'fileName': completion.module_path,
                'line': completion.line,
                'column': completion.column,
            })
    return json.dumps({'id': identifier, 'results': _methods})
