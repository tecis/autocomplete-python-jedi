import os
import io
import re
import sys
import json
import traceback
sys.path.append(os.path.dirname(__file__))
import jedi
# remove jedi from path after we import it so it will not be completed
sys.path.pop(0)

WORD_RE = re.compile(r'\w')
ARGUMENT_RE = re.compile(r'[a-zA-Z0-9_=\*"\']+')

# def __init__(self):
default_sys_path = sys.path
_input = io.open(sys.stdin.fileno(), encoding='utf-8')
devnull = open(os.devnull, 'w')
stdout, stderr = sys.stdout, sys.stderr


# @classmethod
def get_top_level_module(cls, path):
    """Recursively walk through directories looking for top level module.

    Jedi will use current filepath to look for another modules at same
    path, but it will not be able to see modules **above**, so our goal
    is to find the higher python module available from filepath.
    """
    _path, _ = os.path.split(path)
    if _path != path and os.path.isfile(os.path.join(_path, '__init__.py')):
        return cls.get_top_level_module(_path)
    return path


def set_request_config(config):
    """Sets config values for current request.

    This includes sys.path modifications which is getting restored to
    default value on each request so each project should be isolated
    from each other.

    Args:
        config: Dictionary with config values.
    """
    sys.path = default_sys_path
    use_snippets = config.get('useSnippets')
    show_doc_strings = config.get('showDescriptions', True)
    fuzzy_matcher = config.get('fuzzyMatcher', False)
    jedi.settings.case_insensitive_completion = config.get('caseInsensitiveCompletion', True)
    for path in config.get('extraPaths', []):
        if path and path not in sys.path:
            sys.path.insert(0, path)


def process_request(request):
    """Accept serialized request from Atom and write response.
    """
    if not request:
        return
    request = json.loads(request)
    set_request_config(request.get('config', {}))

    path = get_top_level_module(request.get('path', ''))
    if path not in sys.path:
        sys.path.insert(0, path)

    lookup = request.get('lookup', 'completions')  # hmmm

    script = jedi.api.Script(source=request['source'], line=request['line'] + 1,
                             column=request['column'], path=request.get('path', ''))
    rid = request['id']
    arguments = None
    if lookup == 'definitions':
        results = get_definitions(script.goto_assignments())
    elif lookup == 'tooltip':
        results = get_tooltip(script.goto_assignments())
    elif lookup == 'arguments':
        results = []
        arguments = get_arguments(script)
    elif lookup == 'usages':
        results = get_usages(script.usages())
    elif lookup == 'methods':
        results = get_methods(script)
    else:
        results = get_completions(script, request.get('prefix', ''))

    response = {'id': rid, 'results': results}
    if arguments:
        response['arguments'] = arguments
    return response


def write_response(response):
    response = json.dumps(response)
    sys.stdout = stdout
    sys.stdout.write(response + '\n')
    sys.stdout.flush()
    pass


def watch():
    while True:
        try:
            sys.stdout, sys.stderr = devnull, devnull
            process_request(_input.readline())
        except Exception:
            sys.stderr = stderr
            sys.stderr.write(traceback.format_exc() + '\n')
            sys.stderr.flush()
        pass


if __name__ == '__main__':
    if sys.argv[1:]:
        for s in sys.argv[1:]:
            response = process_request(s)
            write_response(response)
    else:
        watch()
