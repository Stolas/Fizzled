#!/usr/bin/env python


#!/usr/bin/env python
from random import choice
from os import listdir
from os.path import isfile, join, abspath
from shutil import move
from time import sleep
import subprocess
import logging

# TODO: Move this to a config file.
# So I can easily log to the centralized server.
logger = logging.getLogger('taskmaster')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

def run(sample_dir, work_dir, crash_dir, recover_time):
    while True:
        file_list = [f for f in listdir(sample_dir) if isfile(join(sample_dir, f))]
        file_list.remove('.ignore')

        # I grab a random one, as next will lead to collitions
        try:
            next_file = choice(file_list)
            file_choice = join(sample_dir, next_file)
            work_file = join(work_dir, next_file)
            crash_file = join(crash_dir, next_file)

            move(file_choice, work_file)

        except IndexError:
            logger.error('Out of files, sleeping for {} seconds'.format(recover_time))
            sleep(recover_time)
            continue

        # Run autopsy
        ret = subprocess.call([abspath("autopsy.py"), work_file])
        if ret:
            logger.info('{} crashed!'.format(work_file))
            move(work_file, crash_file)
        else:
            logger.info('{} didn\'t crash..')


if __name__ == '__main__':
    SAMPLES_DIRECTORY = 'samples'
    WORK_DIRECTORY = 'work'
    CRASH_DIRECTORY = join(WORK_DIRECTORY, 'crash')
    RECOVER_TIME = 10
    run(SAMPLES_DIRECTORY, WORK_DIRECTORY, CRASH_DIRECTORY, RECOVER_TIME)
