#!/usr/bin/env python


#!/usr/bin/env python
from random import choice
from os import listdir
from os.path import isfile, join, abspath
from shutil import move
from time import sleep
import subprocess
import logging
from settings import *

logger = logging.getLogger('taskmaster')

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
    run(SAMPLES_DIRECTORY, WORK_DIRECTORY, CRASH_DIRECTORY, RECOVER_TIME)
