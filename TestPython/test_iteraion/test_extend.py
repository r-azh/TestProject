import itertools

__author__ = 'R.Azh'

_IMAGE_EXTENTIONS = ['png', 'jpg', 'jpeg', 'gif']
_VIDEO_EXTENTIONS = ['flv', 'avi', 'mpg', 'mpeg', '3gp', 'mkv']

# FILE_EXTENTIONS = []
# FILE_EXTENTIONS.extend(_IMAGE_EXTENTIONS + _VIDEO_EXTENTIONS)

FILE_EXTENTIONS = list(itertools.chain(_IMAGE_EXTENTIONS, _VIDEO_EXTENTIONS))
print(FILE_EXTENTIONS)
