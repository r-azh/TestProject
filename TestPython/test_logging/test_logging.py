__author__ = 'R.Azh'

import logging
import os

logging.warning('Watch out!')  # will print a message to the console
# The INFO message doesn’t appear because the default level is WARNING
logging.info('I told you so')  # will not print anything

# The call to basicConfig() should come before any calls to debug(), info() etc. As it’s intended as a one-off simple
#  configuration facility, only the first call will actually do anything: subsequent calls are effectively no-ops.
# you should Clear the handlers and try again:
logging.getLogger('').handlers = []

print('\n########################## logging to a file ###############################')
file_name = '{}/example.log'.format(os.getcwd())
print(file_name)
logging.basicConfig(filename=file_name, level=logging.INFO)    # can add filemode='w' too
# logging.basicConfig(filename=self.SMTP_LOG_FILE, filemode='a', level=logging.INFO)
# logging.FileHandler(self.SMTP_LOG_FILE, mode='a', encoding='utf_8')
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')


print('\n########################## logging with formatting ###############################')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# To display the date and time of an event, you would place ‘%(asctime)s’ in your format string:
formatter = logging.Formatter('- %(levelname)s:‌ %(asctime)s - %(message)s')

# The default format for date/time display (shown above) is ISO8601. If you need more control over the formatting of
# the date/time, provide a datefmt argument to basicConfig, as in this example:
# logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

logger.info('hello from info')
logger.error('hello from error')
logger.debug('hello from debug')




