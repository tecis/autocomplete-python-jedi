def get_usages(usages):
    _usages = []
    for usage in usages:
        _usages.append({
            'name': usage.name,
            'moduleName': usage.module_name,
            'fileName': usage.module_path,
            'line': usage.line,
            'column': usage.column,
        })
    return _usages
