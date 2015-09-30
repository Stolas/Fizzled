# Fizzled Settings file.
# Based on Django.
from os.path import join
from sys import argv
import logging


#
# Directory Configurations
#

SEED_DIRECTORY = 'data'  # This folder keeps the original files.
WORK_DIRECTORY = 'work'  # Files that are in use by workers.

SAMPLES_DIRECTORY = 'samples'  # This is the folder that contains the TODO-Job.s
CRASH_DIRECTORY = join(WORK_DIRECTORY, 'crash')  #  Crash Generators

#
# Test Subject
#

BINARY = "/usr/bin/evince"  # The test subject
ARGUMENTS = [] + argv[1:]  # The argument list

# Fuzzer Engine
MAX_TOTAL_MUTATIONS = 2500  # Amount of testcases to build, None for unlimited.
STRATEGY = 'charlie_miller_fuzz'  # Fuzzing Strategy in use.
TIME_TO_LIVE = 1  # Seconds a bin should live to be alive.
RECOVER_TIME = 10  # Time to wait for the mutator to create more jobs.
DESTRUCTIVE = True  # Destroy the files that don't crash

#
# Debugger
#

# PYDBG_ROOT = '.'  # Note: Windows Only.
# VDB_ROOT = 'vivisect'

#
# Logging
#

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

#
# Deprecated Settings
#

# DATA_DIRECTORY = 'data'
# FILE_TYPE = 'pdf'  # FileType
# TIMESTAMP_FORMAT = "%B %dth, %l:%M %p"

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

# stalker = logging.getLogger('stalker')
# stalker.setLevel(logging.DEBUG)
# stalker.addHandler(stream_handler)
#
# legion = logging.getLogger('legion')
# legion.setLevel(logging.DEBUG)
# legion.addHandler(stream_handler)
