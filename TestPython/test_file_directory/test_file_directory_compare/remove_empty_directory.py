__author__ = 'R.Azh'

import os

def remove_empty_directories_traversal(source_dir, remove_source_dir_tree=False):
    dir_remove_list = {dirpath: filename for dirpath, dirname, filename in os.walk(source_dir)}
    if source_dir in dir_remove_list.keys():
        #dir_remove_list.pop(source_dir, None)  #or
        del dir_remove_list[source_dir]
    if dir_remove_list:
        for d in dir_remove_list:
            print('checking dir: ', d.encode("utf-8"))
            if not dir_remove_list[d]:
                print('------------ removing dir: ', d.encode("utf-8"))
                os.rmdir(d)
    if remove_source_dir_tree:
        print('removing dir tree: ', source_dir.encode("utf-8"))
        import shutil
        shutil.rmtree(source_dir)

remove_empty_directories_traversal('I:/r/_clean up')
