import os
import filecmp
import string
import sys

__author__ = 'root'


def get_files_by_extension_size_recursively(directory):
    directory_contents = {}
    priority = 0
    for dir_path, dir_names, file_names in os.walk(directory):
        priority += 1
        for file in file_names:
            filename, file_extension = os.path.splitext(file)
            file_size = os.path.getsize(f'{dir_path}{os.path.sep}{file}')
            directory_contents.setdefault((file_extension, file_size), []).append((filename, dir_path, priority))
    return directory_contents


def get_files_by_extension_size(directory):
    directory_contents = {}
    priority = 1
    for dir_path, dir_names, file_names in os.walk(directory):
        for file in file_names:
            filename, file_extension = os.path.splitext(file)
            file_size = os.path.getsize(f'{dir_path}{os.path.sep}{file}')
            directory_contents.setdefault((file_extension, file_size), [])\
                .append((filename, dir_path, priority))
        return directory_contents


def get_duplicate_files(directory_list: list, include_subdirectories=False):
    '''
    :param directory_list: [(dir1, 0), (dir2, 1) , (dir2, no_del)]
    lower number in priority means higher -> lower priority will be deleted each time
    :param include_subdirectories: True --> checks subdirectories
    False --> don't check subdirectories
    :return:
    '''

    function_recursive_map = {
        True: get_files_by_extension_size_recursively,
        False: get_files_by_extension_size
    }
    get_files = function_recursive_map[include_subdirectories]
    directory_contents = []
    duplicate_files = set()

    print('Preparing to compare files ...')

    for directory in directory_list:
        directory_contents.append(get_files(directory))

    extension_size_dict = directory_contents[0]
    if len(directory_list) > 1:
        for dir_contents in directory_contents[1:]:
            for extension_size, files in dir_contents.items():
                extension_size_dict.setdefault(extension_size, []).extend(files)

    print('Started comparing files...')
    progress_bar = ProgressBar(len(extension_size_dict))

    for (file_extension, file_size), file_list in extension_size_dict.items():
        progress_bar.next()

        if len(file_list) <= 1:
            continue
        # file_list = list(files)
        for i in range(len(file_list)):
            (ref_file_name, ref_path, ref_priority) = file_list[i]
            ref_file = f'{file_list[i][1]}{os.path.sep}{ref_file_name}{file_extension}'
            if i + 1 == len(file_list):
                break
            for file_name, path, priority in file_list[i+1:]:
                next_file = f'{path}{os.path.sep}{file_name}{file_extension}'
                if next_file in duplicate_files:
                    continue
                print('comparing {} , {}'.format(ref_file, next_file).encode("utf-8"))
                try:
                    if filecmp.cmp(ref_file, next_file):
                        if select_ref_over_file(
                                ref_file_name, ref_path, ref_priority,
                                file_name, path, priority
                        ):
                            duplicate_files.add(next_file)
                        else:
                            duplicate_files.add(ref_file)
                            break
                except Exception as e:
                    print('error', e)
    print(duplicate_files)
    return duplicate_files


def select_ref_over_file(ref_file_name, ref_path, ref_priority, file_name, path, priority):
    ref_is_numeric = file_name_is_numeric(ref_file_name)
    file_is_numeric = file_name_is_numeric(file_name)

    if ref_is_numeric and not file_is_numeric:
        return False
    if not ref_is_numeric and file_is_numeric:
        return True
    if not ref_file_name.endswith(')') and file_name.endswith(')'):
        return True
    if ref_file_name.endswith(')') and not file_name.endswith(')'):
        return False
    if not ref_file_name.endswith('- Copy') and file_name.endswith('- Copy'):
        return True
    if ref_file_name.endswith('- Copy') and not file_name.endswith('- Copy'):
        return False

    if ref_priority < priority:
        return False
    return True


def remove_files(files_list):
    if files_list:
        print('removing {} files :)'.format(len(files_list)))
        for f in files_list:
            if os.path.exists(f):
                print('removing file: ', f.encode("utf-8"))
                os.remove(f)


def remove_duplicate_files(dir_list: list, include_subdirectories=False):
    dup_list = get_duplicate_files(dir_list, include_subdirectories)
    remove_files(dup_list)
    print('removed ', len(dup_list), 'files')
    return len(dup_list)


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def file_name_is_numeric(file_name):
    name_parts = file_name.split("_")

    for i in name_parts:
        for char in string.punctuation:
            i = i.replace(char, "")
        i = i.replace(" ", "")
        i = i.replace("test", "")
        if not is_int(i):
            return False
    return True


class ProgressBar:
    total = None
    run_count = None
    _progressed = 0

    def __init__(self, total, bar_length=40):
        self.total = total
        self.run_count = 0
        self.bar_length = bar_length

    def next(self, progress=1, eta=None):
        self._progressed += progress
        progress = float(self._progressed) / float(self.total)
        block = int(round(self.bar_length * progress))
        sharp_blocks = "#" * block
        dash_blocks = "-" * (self.bar_length - block)
        percentage = int(round(progress * 100, 0))
        if eta:
            text = "\r[{}{} {}% {}/{} ETA: {}".format(
                sharp_blocks, dash_blocks, percentage, self._progressed, self.total, eta
            )
        else:
            text = "\r[{}{} {}% {}/{} ".format(
                sharp_blocks, dash_blocks, percentage, self._progressed, self.total
            )
        sys.stdout.write(text)
        sys.stdout.flush()


def compute_eta(last_mean_time, iteration, current_duration, total_iterations):
    if iteration == 0:
        return current_duration, (current_duration * (total_iterations - 1))

    mean_time = ((last_mean_time * (iteration - 1)) + current_duration) / iteration
    return mean_time, (mean_time * (total_iterations - iteration))


if __name__ == '__main__':
    get_duplicate_files(['D:\\to hard\\mp3\\Celin Dion'], True)
    # remove_duplicate_files(['D://to hard//topc//cleaned up'], True)
    # remove_duplicate_files(['C:\\_Data_\\TED talk'], True)
    # remove_duplicate_files(['D:\\to hard\\mp3', 'D:\\to hard\\mp3\\Mix'], False)

    #remove_duplicate_files('c:/downloads', 'c:/down')
    #remove_duplicate_files('c:/down')
    #remove_duplicate_files('I:/r/_clean up/_clean_up_')
    #remove_duplicate_files('I:/SARA/nn')
    #remove_duplicate_files_traversal('I:/r/_clean up')
    #remove_duplicate_files_traversal('G:\\rezvan\\cooking\\pic')
    #remove_duplicate_files_traversal('Q:\\learn')
    #remove_duplicate_files('H:\\rezvan\\__\\mp3')
    #remove_duplicate_files_traversal('/home/azh/Downloads/topc2')
    #remove_duplicate_files_traversal('N:/fariba/r/tohard/cleanup')
    #remove_duplicate_files_traversal('G:\\rezvan\\cooking\\_movie')
    #remove_duplicate_files_traversal('H:\\rezvan\\0_uni\\Bachelor courses')
    #remove_duplicate_files_traversal('I:\\r\\german\\german movie')
    #remove_duplicate_files('N:/fariba/r/tohard/topc-')
    #remove_duplicate_files('D:\\rez\\__\\cleanup', 'I:\\r\\_clean up\\_clean_up_')
    #remove_duplicate_files('I:/r/_clean up/_clean_up_', 'D:\\rez\\__\\from mobile\\Telegram Video')
	

