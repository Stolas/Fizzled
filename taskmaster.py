#!/usr/bin/env python
from random import choice
from os import listdir, unlink
from os.path import isfile, join, abspath
from shutil import move
from time import sleep
import subprocess
import logging
from settings import *

logger = logging.getLogger('taskmaster')

def run(sample_dir, work_dir, crash_dir, recover_time, destructive):
    if destructive:
        logger.warning('Running in destructive mode')

    while True:
        file_list = [f for f in listdir(sample_dir) if isfile(join(sample_dir, f))]
        file_list.remove('.ignore')

        # I grab a random one, as next will lead to collisions
        try:
            next_file = choice(file_list)
            logger.debug('Trying: {}'.format(next_file))
            file_choice = abspath(join(sample_dir, next_file))
            work_file = abspath(join(work_dir, next_file))
            crash_file = abspath(join(crash_dir, next_file))

            logger.debug('Moving: {} to {}'.format(file_choice, work_file))
            move(file_choice, work_file)

        except IndexError:
            logger.error('Out of files, sleeping for {} seconds'.format(recover_time))
            sleep(recover_time)
            continue

        # Run autopsy
        ret = subprocess.call([abspath("autopsy.py"), work_file])
        if ret:
            logger.info('{} didn\'t crash..'.format(work_file))

            if destructive:
                logger.warning('Deleting {}..'.format(work_file))
                unlink(work_file)
        else:
            logger.info('{} crashed!'.format(work_file))
            logger.debug('Moving: {} to {}'.format(work_file, crash_file))
            move(work_file, crash_file)


if __name__ == '__main__':
    run(SAMPLES_DIRECTORY, WORK_DIRECTORY, CRASH_DIRECTORY,
        RECOVER_TIME, DESTRUCTIVE)
