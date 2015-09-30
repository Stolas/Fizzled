#!/usr/bin/env python

import logging
import math
import sys
from random import choice, randrange
from os import listdir
from os.path import isfile, join, abspath, expanduser
from time import time
from settings import *


logger = logging.getLogger('mutilator')

def charlie_miller_fuzz(buf):
    try:
        # Charlie Miller's fuzzer code:
        fuzz_factor = 250
        num_writes = randrange(math.ceil((float(len(buf)) / fuzz_factor))) + 1

        for _ in range(num_writes):
            r_byte = randrange(256)
            rn = randrange(len(buf))
            buf[rn] = r_byte
        # end of Charlie Miller's code
    except ValueError:
        logger.warning('ValueError, buf is {} bytes long'.format(len(buf)))
        sys.exit(1)

    return buf

def run(seed_dir, samples_dir):
    file_list = [f for f in listdir(seed_dir) if isfile(join(seed_dir, f))]
    file_list.remove('.ignore')

    itr = 0
    while True:
        itr = itr + 1
        try:
            file_choice = join(seed_dir, choice(file_list))
        except IndexError:
            logger.error('No seeds found')
            sys.exit(1)

        fd = open(abspath(file_choice), 'rb')
        buf = bytearray(fd.read())
        fd.close()

        # XXX: Hack a good fuzzy strategy here
        buf = charlie_miller_fuzz(buf)

        new_filename = join(samples_dir, "sample_{}".format(itr))
        logger.debug('Creating file: {}'.format(new_filename))
        fd = open(new_filename, 'wb')
        fd.write(buf)
        fd.close()



if __name__ == '__main__':
    run(SEED_DIRECTORY, SAMPLES_DIRECTORY)
