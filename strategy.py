import math
import sys
import re
import logging
import subprocess
from tempfile import TemporaryFile
from random import randrange, choice

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

def radamsa_fuzz(buf, itr, radamsa_bin):
    fd = TemporaryFile()
    fd.write(buf)
    fd.seek(0, 0)
    process = subprocess.Popen([radamsa_bin], stdin=fd,
              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (buf, err) = process.communicate()
    if err:
        logger.error('Radamsa error: {}'.format(err))
    return buf

def bitflip_fuzz(buf, itr):
    raise NotImplementedError()

def totoro_fuzz(buf, itr):
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
        # -1,
        0,
        # 0x100,
        # 0x1000,
        # 0x3fffffff,
        # 0x7ffffffe,
        # 0x7fffffff,
        # 0x80000000,
        # 0xfffffffe,
        # 0xffffffff,
        0x10000,
        # 0x100000,
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

    rnd_idx = randrange(len(buf))
    rand_byte = buf[rnd_idx]

    # if re.match('[a-zA-Z]', chr(rand_byte)):
    #     # String Match
    #     print('Found a string [%c] @ 0x%x' % (rand_byte, rnd_idx))
    idx = rnd_idx
    buff_start = 0
    buff_end = 0
    e_buff = []

    # Found a string, find the beginning of the string
    if re.match('[A-Za-z]', chr(buf[idx])):
        # print('Found rnd byte [%c] @ 0x%x' % (buf[idx], idx))
        while re.match('[A-Za-z]', chr(buf[idx])):
            # print('Found Str Byte [%c] @ 0x%x' % (buf[idx], idx))
            idx = idx - 1
        idx = idx + 1
        buff_start = idx
        try:
            while re.match('[A-Za-z]', chr(buf[idx])):
                e_buff.append(chr(buf[idx]))
                idx = idx + 1
        except IndexError:
            pass
        buff_end = idx - 1
        fuzz_list = overflow_strings + format_strings
    # Found an int, find the beginning of the int
    elif re.match('\d', chr(buf[idx])):
        # print('Found rnd byte [%c] @ 0x%x' % (buf[idx], idx))
        while re.match('\d', chr(buf[idx])):
            # print('Found Str Byte [%c] @ 0x%x' % (buf[idx], idx))
            idx = idx - 1
        idx = idx + 1
        buff_start = idx
        while re.match('\d', chr(buf[idx])):
            # print('[FOUND INT]')
            e_buff.append(chr(buf[idx]))
            idx = idx + 1
        buff_end = idx - 1
        fuzz_list = int_overflow
    else:
        fuzz_list = [randrange(0xff)]  # Dunno lets make this a random_byte

    if buff_start != buff_end:
        try:
            print('Buff {}-{} found {}'.format(buff_start, buff_end, e_buff))
            buff_begin = bytearray(buf[:buff_start])
            buff_end = bytearray(buf[buff_end:])
            fuzz_value = bytearray(choice(fuzz_list))
            buf = buff_begin + fuzz_value + buff_end
        except MemoryError as ex:
            import pdb ; pdb.set_trace()

    # if itr > 150:
    #     import pdb ; pdb.set_trace()
    # if rand_byte == [A-Z]

    return buf


def nill_fuzz(buf, itr):
    return buf
