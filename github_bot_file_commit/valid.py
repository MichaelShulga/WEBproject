import ast


def is_python_file_valid(f):
    source = f.read()
    f.seek(0)
    try:
        ast.parse(source)
    except Exception:
        return False
    return True


def is_file_damaged(f, original_file):
    source = f.read().decode()
    f.seek(0)
    with open(original_file, 'r') as orig:
        for i in orig.readlines():
            if ('class' in i or 'def' in i) and '#' not in i:
                if i.strip() not in source:
                    return True
    return False
