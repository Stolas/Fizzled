import math
import sys
import logging
from random import randrange

logger = logging.getLogger('mutilator')

def charlie_miller_fuzz(buf, itr):
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

def radamsa_fuzz(buf, itr):
    raise NotImplementedError()

def bitflip_fuzz(buf, itr):
    raise NotImplementedError()

def nill_fuzz(buf, itr):
    return buf
