# Fizzled Settings file.
# Based on Django.
from os.path import join
from sys import argv
import logging

SEED_DIRECTORY = 'data'
DATA_DIRECTORY = 'data'
WORK_DIRECTORY = 'work'
SAMPLES_DIRECTORY = 'samples'
CRASH_DIRECTORY = join(WORK_DIRECTORY, 'crash')
BINARY = "/usr/bin/evince"
ARGUMENTS = [] + argv[1:]
TIME_TO_LIVE = 1
FILE_TYPE = 'pdf'
RECOVER_TIME = 10
TIMESTAMP_FORMAT = "%B %dth, %l:%M %p"
# Set to path where vivisect can be found to use vivisect/vtrace/vdb
# VDB_ROOT = 'vivisect'
# PYDBG_ROOT = '.'  # Note: Windows Only.
STRATEGY = 'charlie_miller_fuzz'
MAX_TOTAL_MUTATIONS = 2500  # Set to None for unlimited.
DESTRUCTIVE = True

# Logging
## Formatting
SIMPLE_FORMAT = logging.Formatter('%(name)s - %(message)s')
CMD_LINE_FORMAT = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
VERBOSE_FORMAT = logging.Formatter('%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s')

## Handlers
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(CMD_LINE_FORMAT)

file_handler = logging.FileHandler('fizzled.log')
file_handler.setLevel(logging.DEBUG)

# syslog_handler = logging.SysLogHandler(address=('localhost', 514))
# syslog_handler.setLevel(logging.DEBUG)
#
# email_handler = logging.SMTPHandler('smtp.gmail.com',
#                                     'from@gmail.com',
#                                     'to@gmail.com',
#                                     'Fizzled Info',
#                                     ('username', 'password'),
#                                     secure=True)
#
# email_handler.setLevel(logging.ERROR)

## Loggers
mutilator = logging.getLogger('mutilator')
mutilator.setLevel(logging.DEBUG)
mutilator.addHandler(stream_handler)
# mutilator.addHandler(syslog_handler)

autopsy = logging.getLogger('autopsy')
autopsy.setLevel(logging.INFO)
autopsy.addHandler(file_handler)
autopsy.addHandler(stream_handler)
# autopsy.addHandler(syslog_handler)

taskmaster = logging.getLogger('taskmaster')
taskmaster.setLevel(logging.DEBUG)
taskmaster.addHandler(stream_handler)
taskmaster.addHandler(file_handler)

### Not in use as of yet.
# stalker = logging.getLogger('stalker')
# stalker.setLevel(logging.DEBUG)
# stalker.addHandler(stream_handler)
#
# legion = logging.getLogger('legion')
# legion.setLevel(logging.DEBUG)
# legion.addHandler(stream_handler)
