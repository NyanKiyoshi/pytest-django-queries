def format_underscore_name_to_human(name):
    if name.startswith('test'):
        _, name = name.split('test', 1)
    return name.replace('_', ' ').strip()
