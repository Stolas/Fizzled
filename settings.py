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
BINARY = "/bin/ls"
ARGUMENTS = ['-L'] + argv[1:]
TIME_TO_LIVE = 1
FILE_TYPE = 'pdf'
RECOVER_TIME = 10
TIMESTAMP_FORMAT = "%B %dth, %l:%M %p"

# Logging
## Formatting
SIMPLE_FORMAT = logging.Formatter('%(name)s - %(message)s')
CMD_LINE_FORMAT = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
VERBOSE_FORMAT = logging.Formatter('%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s')

## Handlers
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(SIMPLE_FORMAT)

file_handler = logging.FileHandler('fizzled.log')
file_handler.setLevel(logging.DEBUG)

syslog_handler = logging.SysLogHandler(address=('localhost', 514))
syslog_handler.setLevel(logging.DEBUG)

email_handler = logging.SMTPHandler('smtp.gmail.com',
                                    'from@gmail.com',
                                    'to@gmail.com',
                                    'Fizzled Info',
                                    ('username', 'password'),
                                    secure=True)

email_handler.setLevel(logging.ERROR)

## Loggers
mutilator = logging.getLogger('mutilator')
mutilator.setLevel(logging.DEBUG)
mutilator.addHandler(stream_handler)
mutilator.addHandler(syslog_handler)

autopsy = logging.getLogger('autopsy')
autopsy.setLevel(logging.DEBUG)
autopsy.addHandler(stream_handler)
autopsy.addHandler(syslog_handler)

taskmaster = logging.getLogger('taskmaster')
taskmaster.setLevel(logging.DEBUG)
taskmaster.addHandler(stream_handler)

stalker = logging.getLogger('stalker')
stalker.setLevel(logging.DEBUG)
stalker.addHandler(stream_handler)

legion = logging.getLogger('legion')
legion.setLevel(logging.DEBUG)
legion.addHandler(stream_handler)
