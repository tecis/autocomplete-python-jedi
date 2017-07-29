def _additional_info(completion):
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


def get_completions(script, prefix=''):
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

    for signature, name, value in self._get_call_signatures(script):
        if not self.fuzzy_matcher and not name.lower().startswith(prefix.lower()):
            continue
        _completion = {
            'type': 'property',
            'rightLabel': self._additional_info(signature)
        }
        # we pass 'text' here only for fuzzy matcher
        if value:
            _completion['snippet'] = '%s=${1:%s}$0' % (name, value)
            _completion['text'] = '%s=%s' % (name, value)
        else:
            _completion['snippet'] = '%s=$1$0' % name
            _completion['text'] = name
            _completion['displayText'] = name
        if self.show_doc_strings:
            _completion['description'] = signature.docstring()
        else:
            _completion['description'] = self._generate_signature(
                signature)
        _completions.append(_completion)

    try:
        completions = script.completions()
    except KeyError:
        completions = []
    for completion in completions:
        if self.show_doc_strings:
            description = completion.docstring()
        else:
            description = self._generate_signature(completion)
        _completion = {
            'text': completion.name,
            'type': self._get_definition_type(completion),
            'description': description,
            'rightLabel': self._additional_info(completion)  # TODO v0.10.2 issue
        }
        if any([c['text'].split('=')[0] == _completion['text']
                for c in _completions]):
            # ignore function arguments we already have
            continue
        _completions.append(_completion)
    return _completions
