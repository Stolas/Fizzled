# Fizzled Settings file.
# Based on Django.
from os.path import join
from sys import argv
import logging


#
# Directory Configurations
#

# The folder keeps the original files.
SEED_DIRECTORY = 'D:\Fizzled\data'

# Files that are in use by workers
WORK_DIRECTORY = 'D:\Fizzled\work'

# The folder that contains the jobs that are to be done.
SAMPLES_DIRECTORY = 'D:\Fizzled\samples'

#  These files genated crashes
CRASH_DIRECTORY = 'D:\Fizzled\crash'

#
# Test Subject
#

# The application to test
BINARY = 'C:\Windows\System32\calc.exe'

# The arguments that are parsed to the application, use {filename} to determine the location of the filename.
ARGUMENTS = ["{filename}"]


#
# Fuzzer Engine
#

# Amount of testcases to build, None for unlimited.
MAX_TOTAL_MUTATIONS = 5000

# Fuzzing Strategy in use.
# Possible choices are:
# - charlie_miller_fuzz	- Uses the 5 Line Charlie Miller Fuzzer
# - radamsa_fuzz	- Uses Radamsa
# - bitflip_fuzz	- Flips a specified bit of the file
# - tororo_fuzz		- Tries to understand the fileformat, and use that
# - smart_fuzz		- Uses content aware fuzzing
# - nill_fuzz
# Or add a custom one to strategy.py
STRATEGY = 'radamsa_fuzz'

# Seconds an application should live to be alive
TIME_TO_LIVE = 1

# Time to wait for the mutator to create more jobs.
RECOVER_TIME = 10

# Destroy the files that don't crash (recommened to use, but use with care)
DESTRUCTIVE = True

# The location for the Radamsa binary
RADAMSA_BIN = 'D:\Fizzled\\radamsa-0.3.exe'

#
# Debugger
#

# Note: Do not forget to pull the submodules (git submodule update --recursive)
# Set the debugger backend to determine crashes and harvest information.
# Valid choices are:
# - vdb     Uses vivisect as debugger.
# - pydbg   This only runs on Windows.
# - ctype   Calls native debuggers functions.
# - None    Use no debugger just check if the application is alive.
DEBUGGER = 'pydbg'

# Location to find PyDbg
PYDBG_ROOT = '.'

# Location to find vivisect
VDB_ROOT = 'vivisect'

#
# API Server
#

# Run the webservice
# Note that all traffic is over HTTP and is unencrypted
RUN_LACKEY = False

# Bind to IP
SERVER_IP = 'localhost'

# Listern on port
SERVER_PORT = 8080

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

lackey = logging.getLogger('lackey')
lackey.setLevel(logging.DEBUG)
lackey.addHandler(stream_handler)
lackey.addHandler(file_handler)

#
# Deprecated Settings
#

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
