from utils import (get_call_signatures, additional_info, generate_signature,
                   get_definition_type)


def get_completions(script, prefix='', fuzzy_matcher=False,
                    show_doc_strings=True):
    """Serialize response to be read from Atom.

    Args:
        script: Instance of jedi.api.Script object.
        identifier: Unique completion identifier to pass back to Atom.
        prefix: String with prefix to filter function arguments.
            Used only when fuzzy matcher turned off.

    Returns:
        Serialized string to send to Atom.
    """
    _completions = []

    for signature, name, value in get_call_signatures(script):
        if not fuzzy_matcher and not name.lower().startswith(prefix.lower()):
            continue
        _completion = {
            'type': 'property',
            'rightLabel': additional_info(signature)
        }
        # we pass 'text' here only for fuzzy matcher
        if value:
            _completion['snippet'] = '%s=${1:%s}$0' % (name, value)
            _completion['text'] = '%s=%s' % (name, value)
        else:
            _completion['snippet'] = '%s=$1$0' % name
            _completion['text'] = name
            _completion['displayText'] = name
        if show_doc_strings:
            _completion['description'] = signature.docstring()
        else:
            _completion['description'] = generate_signature(signature)
        _completions.append(_completion)

    try:
        completions = script.completions()
    except KeyError:
        completions = []

    for completion in completions:
        if show_doc_strings:
            description = completion.docstring()
        else:
            description = generate_signature(completion)
        _completion = {
            'text': completion.name,
            'type': get_definition_type(completion),
            'description': description,
            'rightLabel': additional_info(completion)  # TODO v0.10.2 issue
        }
        if any([c['text'].split('=')[0] == _completion['text']
                for c in _completions]):
            # ignore function arguments we already have
            continue
        _completions.append(_completion)
    return _completions
