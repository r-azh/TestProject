__author__ = 'R.Azh'

# http://www.bogotobogo.com/

import os

# home = os.path.expanduser("~")
# root_dir = os.path.join(home, "Documents/Work")
root_dir = os.path.curdir
print('dir: ', root_dir)
cmake_path = os.path.join(root_dir, "CMakeLists.txt")


# make target list
def make_target_list():
    target_tag = b"set(TARGET_NAME"
    target_list = []
    for dirpath, dirs, files in os.walk(root_dir):
        if "CMakeLists.txt" in files:
            for f in files:
                cmake_path = os.path.join(dirpath, f)
                with open(cmake_path, 'rb') as lines:
                    for line in lines:
                        if target_tag in line:
                            target = line[line.find(target_tag)+len(target_tag)+1:line.find(b")")]
                            target_list.append(target.strip(b'"'))
    return target_list


# writing csv
def write_csv(t):
    import csv
    with open('tf.csv', 'w') as f:
        w = csv.writer(f, delimiter=' ')
        w.writerow(t)


if __name__ == '__main__':
    target = make_target_list()
    print(target)
    write_csv(target)
