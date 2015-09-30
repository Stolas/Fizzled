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

def totoro_fuz(buf, itr):
    ##                                    ##
    #  _____            Tororo             #
    # /     \             is fuzzy         #
    # vvvvvvv  /|__/|       I need a name. #
    #    I   /O,O   |                      #
    #    I /_____   |      /|/|            #
    #   J|/^ ^ ^ \  |    /00  |    _//|    #
    #    |^ ^ ^ ^ |W|   |/^^\ |   /oo |    #
    #     \m___m__|_|    \m_m_|   \mm_|    #
    ##                                    ##

    int_overflow = [
        -1,
        0,
        0x100,
        0x1000,
        0x3fffffff,
        0x7ffffffe,
        0x7fffffff,
        0x80000000,
        0xfffffffe,
        0xffffffff,
        0x10000,
        0x100000,
    ]

    format_strings = [
        "%s%p%x%d",
        "%p%p%p%p",
        "%x%x%x%x",
        "%d%d%d%d",
        "%s%s%s%s",
        "%99999999999s",
        "%08x",
        "%20d",
        "%20n",
        "%20x",
        "%20s",
        "XXXXX.%p",
        "%08x.%08x.%08x.%08x.%08x\n",
        "XXX0_%08x.%08x.%08x.%08x.%08x\n",
        "%.16705u%2\$hn",
        "\x10\x01\x48\x08_%08x.%08x.%08x.%08x.%08x|%s|"
    ]

    overflow_strings = [
        "A"*1024,
        "A"*2048,
        "A"*4096,
        "A"*8192,
    ]

    rnd_idx = randrage(len(buf))
    rand_byte = buf[rnd_idx]
    # if rand_byte == [A-Z]


def nill_fuzz(buf, itr):
    return buf
