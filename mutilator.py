#!/usr/bin/env python

import logging
from random import choice, randrange
from os import listdir
from os.path import isfile, join, abspath, expanduser
from time import time

# TODO: Move this to a config file.
# So I can easily log to the centralized server.
logger = logging.getLogger('mutilator')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

def charlie_miller_fuzz(buf):
    # Charlie Miller's fuzzer code:
    num_writes = randrange(math.ceil((float(len(buf)) / fuzz_factor))) + 1

    for _ in range(num_writes):
        r_byte = randrange(256)
        rn = randrange(len(buf))
        buf[rn] = r_byte
    # end of Charlie Miller's code
    return buf

def run(seed_dir, samples_dir):
    file_list = [f for f in listdir(seed_dir) if isfile(join(seed_dir, f))]
    file_list.remove('.ignore')

    try:
        while True:
            file_choice = join(seed_dir, choice(file_list))

            fd = open(abspath(file_choice), 'rb')
            buf = bytearray(fd.read())
            fd.close()

            # XXX: Hack a good fuzzy strategy here
            buf = charlie_miller_fuzz(buf)

            new_filename = join(samples_dir, time())
            logger.debug('Creating file: {}'.format(new_filename))
            fd = open(new_filename, 'wb')
            fd.write(buf)
            fd.close()
    except Exception as ex:
        logger.fatal(ex)


if __name__ == '__main__':
    SEED_DIR = 'data'
    SAMPLES_DIR = 'samples'
    run(SEED_DIR, SAMPLES_DIR)
