import os
__author__ = 'R.Azh'


def merge_directories_traversal(source_dir, target_dir=None):
    if not target_dir:
        target_dir = source_dir
    dir_paths = {dirpath: filename for dirpath, dirname, filename in os.walk(source_dir)}
    if dir_paths:
        if not os.path.exists(target_dir):
                os.mkdir(target_dir)
    for dir in dir_paths.keys():
        print('moving file from {} to {}'.format(dir.encode("utf-8"), target_dir.encode("utf-8")))
        dir_contents = dir_paths[dir]
        if dir_contents:
            for f in dir_contents:
                filename = os.path.basename(f)
                dest_file = '{}/{}'.format(target_dir, filename)
                i = 0
                while os.path.exists(dest_file):
                    i += 1
                    base, extension = os.path.splitext(filename)
                    if extension:
                        extension = '.{}'.format(extension)
                    dest_file = '{}/{}_{}{}'.format(target_dir, base, i, extension)
                os.rename('{}/{}'.format(dir, f), dest_file)

    if not target_dir:
        dir_remove_list = {dirpath: filename for dirpath, dirname, filename in os.walk(source_dir)}
        dir_remove_list.remove(source_dir)
        if dir_remove_list:
            for d in dir_remove_list:
                print('checking dir: ', d.encode("utf-8"))
                if not dir_remove_list[d]:
                    print('removing dir: ', d.encode("utf-8"))
                    os.rmdir(d)
    else:
        print('removing dir tree: ', source_dir.encode("utf-8"))
        import shutil
        shutil.rmtree(source_dir)

merge_directories_traversal('I:/r/nn/o', 'I:/r/nn/oo')
