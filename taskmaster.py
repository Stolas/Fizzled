#!/usr/bin/env python
from random import choice
from os import listdir, unlink
from os.path import isfile, join, abspath
from shutil import move
from autopsy import run as run_autopsy
from time import sleep
import sys
import subprocess
import logging

logger = logging.getLogger('taskmaster')

def run(binary, args, ttl, sample_dir, work_dir, crash_dir, recover_time, destructive):
    if destructive:
        logger.warning('Running in destructive mode')

    while True:
        file_list = [f for f in listdir(sample_dir) if isfile(join(sample_dir, f))]
        try:
            file_list.remove('.ignore')
        except ValueError:
            pass

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
        if isinstance(args, str):
            args = [args]

        ret = run_autopsy(binary, args + [work_file], ttl)

        if ret:
            logger.info('{} didn\'t crash..'.format(work_file))

            if destructive:
                logger.warning('Deleting {}..'.format(work_file))
                try:
                    unlink(work_file)
                except WindowsError:
                    logger.error('File in use, can\'t delete it.')
        else:
            logger.info('{} crashed!'.format(work_file))
            logger.debug('Moving: {} to {}'.format(work_file, crash_file))
            move(work_file, crash_file)


if __name__ == '__main__':
    from settings import *
    run(BINARY, ARGUMENTS, TIME_TO_LIVE,
        SAMPLES_DIRECTORY, WORK_DIRECTORY,
        CRASH_DIRECTORY, RECOVER_TIME, DESTRUCTIVE)
