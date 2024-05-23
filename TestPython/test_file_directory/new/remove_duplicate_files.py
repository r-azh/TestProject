import os
import filecmp
from pprint import pprint

__author__ = 'root'


def get_duplicate_files(dir1, dir2=None):
    d1_contents = set(os.listdir(dir1))
    if not dir2:
        dir2 = dir1
        d2_contents = d1_contents
    else:
        d2_contents = set(os.listdir(dir2))
    #print(d1_contents, '\n', len(d1_contents))
    #print(d2_contents, '\n', len(d2_contents))
    duplicate_files = []
    d1_extensions = {}
    d2_extensions = {}
    # filter based on file extentions too
    for f1 in d1_contents:
        f1_full_name = '{}/{}'.format(dir1, f1)
        filename, file_extension = os.path.splitext(f1_full_name)
        file_size = os.path.getsize(f1_full_name)
        if (file_extension.lower(), file_size) not in d1_extensions.keys():
            d1_extensions[(file_extension.lower(), file_size)] = [f1_full_name]
        else:
            d1_extensions[(file_extension.lower(), file_size)].append(f1_full_name)
    if dir2:
        for f2 in d2_contents:
            f2_full_name = '{}/{}'.format(dir2, f2)
            file_extension = os.path.splitext(f2_full_name)[1]
            file_size = os.path.getsize(f2_full_name)
            if (file_extension, file_size) not in d2_extensions.keys():
                d2_extensions[(file_extension, file_size)] = [f2_full_name]
            else:
                d2_extensions[(file_extension, file_size)].append(f2_full_name)
    else:
        d2_extensions = d1_extensions

    for ext in d1_extensions.keys():
        if ext in d2_extensions.keys():
            for f1 in d1_extensions[ext]:
                for f2 in d2_extensions[ext]:
                    print(' **** ', ext, ' ****')
                    if f1 != f2:
                        print('comparing {} , {}'.format(f1, f2).encode("utf-8"))
                        try:
                            # if functional_way_compare(f1,f2):  # dont work for copies
                            if filecmp.cmp(f1, f2):
                                duplicate_files.append(f2)
                                if dir1 == dir2:
                                    d1_extensions[ext].remove(f2)
                        except Exception as e:
                            print('error', e)
    #print(duplicate_files)
    return duplicate_files


def functional_way_compare(filename1, filename2):
    import itertools, functools, operator
    # "Do the two files have exactly the same contents?"
    try:
        with open(filename1, "rb") as fp1, open(filename2, "rb") as fp2:
            if os.fstat(fp1.fileno()).st_size != os.fstat(fp2.fileno()).st_size:
                return False
            fp1_reader = functools.partial(fp1.read, 4096)
            fp2_reader = functools.partial(fp2.read, 4096)
            cmp_pairs = itertools.zip(iter(fp1_reader, ''), iter(fp2_reader, ''))
            inequalities = itertools.starmap(operator.ne, cmp_pairs)
            return not any(inequalities)
    except Exception as e:
        print('error', e)


def remove_files(files_list):
    if files_list:
        print('removing {} files :)'.format(len(files_list)))
        for f in files_list:
            if os.path.exists(f):
                print('removing file: ', f.encode("utf-8"))
                os.remove(f)


def remove_duplicate_files(dir1, dir2=None):
    dup_list = []
    dup_list = get_duplicate_files(dir1, dir2) if dir2 else get_duplicate_files(dir1)
    print('removed ', len(dup_list), 'files')
    remove_files(dup_list)
    return len(dup_list)


def remove_duplicate_files_traversal(dir):
    dir_paths = [dirpath for dirpath, dirname, filename in os.walk(dir)]
    # import itertools
    # for a, b in itertools.combinations(dir_paths, 2):
    #     remove_duplicate_files(a, b)
    # or

    count = 0
    for i in range(len(dir_paths)):
        remove_duplicate_files(dir_paths[i])
        for j in range(i+1, len(dir_paths)):
            try:
                count += remove_duplicate_files(dir_paths[j], dir_paths[i])
            except Exception as e:
                print('error', e)
    print('removed ', count, ' files total')


if __name__ == '__main__':
    remove_duplicate_files('H:\\mp3\\deutch')
    #remove_duplicate_files_traversal('H:\\rezvan\\0_uni\\Bachelor courses')


