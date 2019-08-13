import os

_PROJECT_PATH = os.path.realpath(__file__)
for i in range(3):
    _PROJECT_PATH = os.path.dirname(_PROJECT_PATH)


def get_relative_path(rel_dir=None, file_name=None, make_dirs=True):
    if rel_dir is not None:
        result = os.path.join(_PROJECT_PATH, rel_dir)
        if make_dirs and not os.path.exists(result):
            os.mkdir(result)
    else:
        result = _PROJECT_PATH

    if file_name is not None:
        result = os.path.join(result, file_name)

    return result


def directory_traverse(relative_directory):
    file_list = []
    for dirpath, dirs, files in os.walk(relative_directory):
        file_list.extend([(dirpath, file) for file in files])
    return file_list


def import_module_from_file(base_path, module_path, module_name):
    # this won't work because import is called inside a function scope
    if module_name.endswith('.py') and not module_name.startswith('__'):
        import_path = module_path.replace(base_path, '').replace(os.path.sep, '.')

        exec(f'from {import_path}.{module_name.replace(".py", "")} import *')


if __name__ == '__main__':
    base_path = get_relative_path('test_file_directory')
    files = directory_traverse(base_path)
    for m in files:
        import_module_from_file(base_path, *m)       # this won't work because import is called inside a function scope
    print(files)

