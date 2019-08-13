import os

__author__ = 'root'


def merge_same_name_directories_traversal(source_dir, target_dir):
    dir_paths = {dirpath: filename for dirpath, dirname, filename in os.walk(source_dir)}
    dir_names = {}
    for folder_name in dir_paths.keys():
        dir_name = os.path.basename(folder_name)
        if dir_name not in dir_names.keys():
            dir_names[dir_name] = [folder_name]
        else:
            dir_names[dir_name].append(folder_name)

    dir_remove_list = []
    if dir_names:
        if not os.path.exists(target_dir):
                os.mkdir(target_dir)
        for folder_name in dir_names.keys():
            new_dir = '{}/{}'.format(target_dir, folder_name)
            if not os.path.exists(new_dir):
                os.mkdir(new_dir)
            for dir in dir_names[folder_name]:
                print('moving file from {} to {}'.format(dir.encode("utf-8"), new_dir.encode("utf-8")))
                dir_contents = dir_paths[dir]
                if dir_contents:
                    for f in dir_contents:
                        filename = os.path.basename(f)
                        dest_file = '{}/{}'.format(new_dir, filename)
                        i = 0
                        while os.path.exists(dest_file):
                            i += 1
                            base, extension = os.path.splitext(filename)
                            if extension:
                                extension = '.{}'.format(extension)
                            dest_file = '{}/{}_{}{}'.format(new_dir, base, i, extension)
                        os.rename('{}/{}'.format(dir, f), dest_file)
                else:
                    dir_remove_list.append(dir)
    import shutil
    shutil.rmtree(source_dir)
    # os.rmdir(dir)

#merge_same_name_directories_traversal('/home/azh/Downloads/topc2', '/home/azh/Downloads/topc3')
# merge_same_name_directories_traversal('I:/SARA/n', 'I:/SARA/nn')
merge_same_name_directories_traversal('D://to hard//topc//clean up', 'D://to hard//topc//cleaned up')
