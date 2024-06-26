import os
import string
from pathlib import Path

import mutagen
from mutagen.easyid3 import EasyID3

illegal_characters = string.punctuation.replace('_', '').replace('-', '')


def remove_illegal_chars(name):
    for char in illegal_characters:
        if char in name:
            name = name.replace(char, ' ')
    return name


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


def rename_mp3(dir):
    renamed_count = 0
    dir_contents = os.listdir(dir)
    empty_list = []
    for file in dir_contents:
        file_full_name = '{}/{}'.format(dir, file)
        filename, file_extension = os.path.splitext(file_full_name)
        if file_extension.lower() != '.mp3':
            continue

        if not file_name_is_numeric(os.path.split(filename)[-1]):
            continue

        try:
            meta = EasyID3(file_full_name)
            title = meta.get('title', [])
            artist = meta.get('artist', [])
            album = meta.get('album', [])

            if len(title) == 0 and len(artist) == 0:
                empty_list.append(file)
                continue

            new_name = '_'.join(title + artist)
            new_name = remove_illegal_chars(new_name)
            if new_name == '':
                print('empty name for: ', file.encode('utf-8'))
                continue

            new_file_path = '{}/{}'.format(dir, new_name + '.mp3')
            if not os.path.exists(new_file_path):
                os.rename(file_full_name, new_file_path)
                renamed_count += 1
            else:
                i = 1
                while os.path.exists(new_file_path):
                    new_name = new_name + '-' + str(i)
                    new_file_path = '{}/{}'.format(dir, new_name + '.mp3')
                    i += 1
                os.rename(file_full_name, new_file_path)
                renamed_count += 1
            # print(new_name.encode('utf-8'))

        # except mutagen.id3.ID3NoHeaderError:
            # meta = mutagen.File(file_full_name._str, easy=True)
            # meta.add_tags()

        except Exception as ex:
            print('Error: ', file.encode('utf-8'), ex)

    print('No info for files: ')
    print(empty_list)
    print('Renamed %s files' % renamed_count)


rename_mp3('H:\\mp3\\deutch'.replace('\\', '/'))
# rename_mp3('.')

# audio['title'] = u"Example Title"
# audio['artist'] = u"Me"
# audio['album'] = u"My album"
# audio['composer'] = u"" # clear
# audio.save()