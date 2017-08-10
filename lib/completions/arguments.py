from .utils import get_call_signatures


def get_arguments(script, use_snippets):
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
        elif use_snippets == 'all':
            arg = '%s=${%s:%s}' % (name, i, value)
        else:
            continue
        if name not in seen:
            seen.add(name)
            arguments.append(arg)
        i += 1
    snippet = '%s$0' % ', '.join(arguments)
    return snippet
