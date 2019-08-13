from __future__ import with_statement

__author__ = 'R.Azh'
import os
import filecmp
from pprint import pprint


def mkfile(filename, body=None):
    with open(filename, 'w') as f:
        f.write(body or filename)
    return


def make_example_dir(top):
    if not os.path.exists(top):
        os.mkdir(top)
    curdir = os.getcwd()
    os.chdir(top)

    os.mkdir('dir1') if not os.path.exists('dir1') else None
    os.mkdir('dir2') if not os.path.exists('dir2') else None

    mkfile('dir1/file_only_in_dir1') if not os.path.isfile('dir1/file_only_in_dir1') else None
    mkfile('dir2/file_only_in_dir2') if not os.path.isfile('dir2/file_only_in_dir2') else None

    os.mkdir('dir1/dir_only_in_dir1') if not os.path.exists('dir1/dir_only_in_dir1') else None
    os.mkdir('dir2/dir_only_in_dir2') if not os.path.exists('dir2/dir_only_in_dir2') else None

    os.mkdir('dir1/common_dir') if not os.path.exists('dir1/common_dir') else None
    os.mkdir('dir2/common_dir') if not os.path.exists('dir2/common_dir') else None

    mkfile('dir1/common_file', 'this file is the same') if not os.path.isfile('dir1/common_file') else None
    mkfile('dir2/common_file', 'this file is the same') if not os.path.isfile('dir2/common_file') else None

    mkfile('dir1/not_the_same') if not os.path.isfile('dir1/not_the_same') else None
    mkfile('dir2/not_the_same') if not os.path.isfile('dir2/not_the_same') else None

    mkfile('dir1/file_in_dir1', 'This is a file in dir1') if not os.path.isfile('dir1/file_in_dir1') else None
    os.mkdir('dir2/file_in_dir1') if not os.path.exists('dir2/file_in_dir1') else None

    os.chdir(curdir)
    return


def compare_files():
    print('common_file :', end=' ')
    print(filecmp.cmp('example/dir1/common_file',
                      'example/dir2/common_file'),
          end=' ')
    print(filecmp.cmp('example/dir1/common_file',
                      'example/dir2/common_file',
                      shallow=False))

    print('not_the_same:', end=' ')
    print(filecmp.cmp('example/dir1/not_the_same',
                      'example/dir2/not_the_same'),
          end=' ')
    print(filecmp.cmp('example/dir1/not_the_same',
                      'example/dir2/not_the_same',
                      shallow=False))

    print('identical   :', end=' ')
    print(filecmp.cmp('example/dir1/file_only_in_dir1',
                      'example/dir1/file_only_in_dir1'),
          end=' ')
    print(filecmp.cmp('example/dir1/file_only_in_dir1',
                      'example/dir1/file_only_in_dir1',
                      shallow=False))

    # filecmp.cmp(filename1, filename2, shallow=False)


def find_mathces():
    # Determine the items that exist in both directories
    d1_contents = set(os.listdir('example/dir1'))
    d2_contents = set(os.listdir('example/dir2'))
    common = list(d1_contents & d2_contents)
    common_files = [
        f
        for f in common
        if os.path.isfile(os.path.join('example/dir1', f))
    ]
    print('Common files:', common_files)

    # Compare the directories
    match, mismatch, errors = filecmp.cmpfiles(
        'example/dir1',
        'example/dir2',
        common_files,
    )
    print('Match       :', match)
    print('Mismatch    :', mismatch)
    print('Errors      :', errors)


def directory_compare():
    dc = filecmp.dircmp('example/dir1', 'example/dir2')
    dc.report()
    print('\n full closure \n')
    dc.report_full_closure()

    # Besides producing printed reports, dircmp calculates lists of files that can be used in programs directly.
    #  Each of the following attributes is calculated only when requested, so creating a dircmp instance does not
    # incur overhead for unused data.

    print('\nLeft:')
    pprint(dc.left_list)

    print('\nRight:')
    pprint(dc.right_list)

    # The inputs can be filtered by passing a list of names to ignore to the constructor. By default the names RCS, CVS,
    #  and tags are ignored.

    dc = filecmp.dircmp('example/dir1', 'example/dir2',
                        ignore=['common_file'])

    print('Left:')
    pprint(dc.left_list)

    print('\nRight:')
    pprint(dc.right_list)

    # The names of files common to both input directories are saved in common, and the files unique to each directory
    #  are listed in left_only, and right_only.

    dc = filecmp.dircmp('example/dir1', 'example/dir2')
    print('Common:')
    pprint(dc.common)

    print('\nLeft:')
    pprint(dc.left_only)

    print('\nRight:')
    pprint(dc.right_only)

    # The common members can be further broken down into files, directories and “funny” items (anything that has a
    # different type in the two directories or where there is an error from os.stat()).

    dc = filecmp.dircmp('example/dir1', 'example/dir2')
    print('Common:')
    pprint(dc.common)

    print('\nDirectories:')
    pprint(dc.common_dirs)

    print('\nFiles:')
    pprint(dc.common_files)

    print('\nFunny:')
    pprint(dc.common_funny)

    # The differences between files are broken down similarly.

    dc = filecmp.dircmp('example/dir1', 'example/dir2')
    print('Same      :', dc.same_files)
    print('Different :', dc.diff_files)
    print('Funny     :', dc.funny_files)

    # Finally, the subdirectories are also saved to allow easy recursive comparison.
    # The attribute subdirs is a dictionary mapping the directory name to new dircmp objects.

    dc = filecmp.dircmp('example/dir1', 'example/dir2')
    print('Subdirectories:')
    print(dc.subdirs)


# def functional_way_compare(filename1, filename2):
#     import itertools, functools, operator
#     # "Do the two files have exactly the same contents?"
#     with open(filename1, "rb") as fp1, open(filename2, "rb") as fp2:
#         if os.fstat(fp1.fileno()).st_size != os.fstat(fp2.fileno()).st_size:
#             return False # different sizes ∴ not equal
#         fp1_reader = functools.partial(fp1.read, 4096)
#         fp2_reader = functools.partial(fp2.read, 4096)
#         cmp_pairs = itertools.zip(iter(fp1_reader, ''), iter(fp2_reader, ''))
#         inequalities = itertools.starmap(operator.ne, cmp_pairs)
#         return not any(inequalities)

if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__) or os.getcwd())
    make_example_dir('example')
    make_example_dir('example/dir1/common_dir')
    make_example_dir('example/dir2/common_dir')
    compare_files()
    find_mathces()
    directory_compare()

    # import sys
    # result = functional_way_compare(sys.argv[1], sys.argv[2])
    # print(result)