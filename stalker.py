#!/usr/bin/env python
import sys
from random import choice, randrange
from os import listdir
from os.path import isfile, join, abspath, expanduser
from time import time, strftime
import logging

# Change this to your vdb path
VDB_ROOT = "vivisect"
sys.path.append(VDB_ROOT)

import vtrace
import vdb
from envi.archs.i386 import *
from settings import *

logger = logging.getLogger('stalker')

def run(data_dir, binary, args, time_format):
    file_list = [f for f in listdir(data_dir) if isfile(join(data_dir, f))]
    file_list.remove('.ignore')

    log_file = open('stalker.log', 'w')
    log_file.write("Fuzzy Stalking {}\n".format(binary))
    log_file.write("Got {} files to walkthrough.\n".format(len(file_list)))
    log_file.write("Current time: {}\n".format(strftime(time_format)))
    log_file.write("Start:\n")

    for stalk_file in file_list:
        fuzzy_hash = run_trace(binary, args + [stalk_file])
        log_file.write("{} - {}\n".format(fuzzy_hash, stalk_file))

    log_file.write("Finished at: {}\n".format(strftime(time_format)))
    log_file.close()


def run_trace(binary, args):
    trace = vtrace.getTrace()
    trace.setMode("FastStep", True)

    execute_path = " ".join([binary] + args)
    trace.execute(execute_path)
    while trace.isRunning():
        pass
        # print(trace.getRegister(REG_EIP))
        # run till call

    # Now the program has quit.
    # make a fuzzy hash.
    fuzzy_hash = None

    return fuzzy_hash

if __name__ == '__main__':
    run(DATA_DIRECTORY, BINARY, ARGUMENTS, TIMESTAMP_FORMAT)
