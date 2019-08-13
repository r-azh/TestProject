__author__ = 'R.Azh'

#  encode videos using ffmpeg

import subprocess, os

# sudo mkdir /var/www
# sudo mkdir /var/www/.fonts
# sudo apt-get install ffmpeg
# sudo cp /home/azh/bin/{ffmpeg,ffprobe,ffserver} /usr/local/bin    # for permission denied error



#-------------------------------------------------------------------------------
# CONFIGURABLE SETTINGS
#-------------------------------------------------------------------------------

# controls the quality of the encode
CRF_VALUE = '21'

# h.264 profile
PROFILE = 'high'

# encoding speed:compression ratio
PRESET = 'fast'

# path to ffmpeg bin
# FFMPEG_PATH = '/usr/local/bin/ffmpeg'
FFMPEG_PATH = 'ffmpeg'


# font dir
FONT_DIR = '/var/www/.fonts'

##------------------------------------------------------------------------------
# encoding script
##------------------------------------------------------------------------------


def process():
    cwd = os.getcwd()
    # cwd = '/home/azh/Downloads'

    # get a list of files that have the extension mkv
    # file_list = filter(lambda f: f.split('.')[-1] == 'mkv', os.listdir(cwd))
    file_list = filter(lambda f: f.split('.')[-1] == 'mov', os.listdir(cwd))
    file_list = sorted(file_list)

    # encode each file
    for file in file_list:
        encode(file)


def encode(file):
    name = ''.join(file.split('.')[:-1])
    # subtitles = 'temp.ass'.format(name)
    output = '{}.mp4'.format(name)

    try:
        command = [FFMPEG_PATH, '-i', file, '-codec:v', 'libx264', '-profile:v', 'high', '-codec:a', 'libfdk_aac']  # config for all html5
        # command = [FFMPEG_PATH, '-i', file,
        #     '-c:v', 'libx264', '-preset', PRESET, '-profile:v', PROFILE]
            # '-c:v', 'libx264', '-tune', 'animation', '-preset', PRESET, '-profile:v', PROFILE, '-crf', CRF_VALUE]

        # create a folder called attachments and symlink it to FONT_DIR
        # extract attachments
        # if not os.path.exists('attachments'):
        #     subprocess.call(['mkdir', 'attachments'])
        # subprocess.call(['rm', '-fr', FONT_DIR])
        # subprocess.call(['ln', '-s', '{}/attachments'.format(os.getcwd()), FONT_DIR])
        # os.chdir('attachments')
        # subprocess.call([FFMPEG_PATH, '-dump_attachment:t', '', '-i', '../{}'.format(file)])
        # os.chdir('..')

        # extract ass subtitles and and subtitle into command
        # subprocess.call([FFMPEG_PATH, '-i', file, subtitles])
        # if os.path.getsize(subtitles) > 0:
        #     command += ['-vf', 'ass={}'.format(subtitles)]

        command += ['-c:a', 'copy']     # if audio is using AAC copy it - else encode it
        command += ['-threads', '8', output]    # add threads and output
        subprocess.call(command)    # encode the video!

    finally:
        pass
        # always cleanup even if there are errors
        # subprocess.call(['rm', '-fr', 'attachments'])
        # subprocess.call(['rm', '-f', FONT_DIR])
        # subprocess.call(['rm', '-f', subtitles])


if __name__ == "__main__":
    process()

# ffmpeg -i SampleVideo_720x480_2mb.mkv  -map 0 -c:v libx264 -c:a copy sample.mp4  ### above sample

# ffmpeg -i your_video_path -qscale 4 -vcodec libx264 -f mp4 your_new_video_path.mp4   ### for mp4
# ffmpeg -i your_video_path -b 1500k -vcodec libvpx -acodec libvorbis -ab 160000 -f webm -g 30
# your_new_video_path.webm  ### for webm
# ffmpeg -i neha.avi -acodec libvorbis output.ogg     #### for ogg

# ffmpeg -i source.mp4 -c:v libx264 -ar 22050 -crf 28 destinationfile.flv   ### for flv

# mp4_configs = ['-codec:v', 'libx264', '-profile:v', 'high', '-codec:a', 'libfdk_aac'] # config for all browsers
# except IE in html5

