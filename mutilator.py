#!/usr/bin/env python

import logging
import sys
from random import choice
from os import listdir
from os.path import isfile, join, abspath, expanduser
from time import strftime
from strategy import *
from settings import *


logger = logging.getLogger('mutilator')


def run(seed_dir, samples_dir):
    file_list = [f for f in listdir(seed_dir) if isfile(join(seed_dir, f))]
    file_list.remove('.ignore')

    itr = 0
    logger.info('Starting Mutilator with {}'.format(STRATEGY))
    while True:
        if MAX_TOTAL_MUTATIONS:
            if MAX_TOTAL_MUTATIONS < itr:
                logger.warning('Reached the limit of {} mutations.'.format(MAX_TOTAL_MUTATIONS))
                sys.exit(0)
        itr = itr + 1
        try:
            file_choice = join(seed_dir, choice(file_list))
        except IndexError:
            logger.error('No seeds found')
            sys.exit(1)

        fd = open(abspath(file_choice), 'rb')
        buf = bytearray(fd.read())
        fd.close()

        # Load & Run Mutation Strategy
        try:
            buf = globals()[STRATEGY](buf, itr)
        except KeyError:
            logger.fatal('Strategy {} does not exist.'.format(STRATEGY))

        stamp = strftime('%y%m%d%H%M%S')
        new_filename = join(samples_dir, "sample_{}_{}".format(stamp, itr))
        logger.debug('Creating file: {}'.format(new_filename))
        fd = open(new_filename, 'wb')
        fd.write(buf)
        fd.close()



if __name__ == '__main__':
    run(SEED_DIRECTORY, SAMPLES_DIRECTORY)
