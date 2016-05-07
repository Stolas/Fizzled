#!/usr/bin/env python

from argparse import ArgumentParser
from threading import Thread
from time import sleep
import sys
import mutilator
import taskmaster
import autopsy
import lackey

AVAILABLE_TOOLS = ['mutilator', 'taskmaster', 'autopsy', 'auto']
BANNER = " ______ _         _          _\n"\
         "|  ____(_)       | |        | |\n"\
         "| |__   _ _______| | ___  __| |\n"\
         "|  __| | |_  /_  / |/ _ \/ _` |\n"\
         "| |    | |/ / / /| |  __/ (_| |\n"\
         "|_|    |_/___/___|_|\___|\__,_|\n"


class Fizzled():
    def __init__(self):
        # Parse Args
        parser = ArgumentParser()
        parser.add_argument('--tool', choices=AVAILABLE_TOOLS, required=True)
        parser.add_argument('--settings', default='settings')
        parser.add_argument('--daemonize', action='store_true')
        parser.add_argument('--no-banner', action='store_true')
        # TODO: More and less verbose

        args = parser.parse_args()

        self.tool = args.tool
        self.settings_file = args.settings

        if args.daemonize:
            raise NotImplemented()

        # Parse Settings
        settings = __import__(self.settings_file)
        self.seed_dir = settings.SEED_DIRECTORY
        self.work_dir = settings.WORK_DIRECTORY
        self.samples_dir = settings.SAMPLES_DIRECTORY
        self.crash_dir = settings.CRASH_DIRECTORY
        self.binary = settings.BINARY
        self.fuzz_args = settings.ARGUMENTS
        self.ttl = settings.TIME_TO_LIVE
        self.recover_time = settings.RECOVER_TIME
        self.destructive = settings.DESTRUCTIVE
        self.debugger = settings.DEBUGGER
        self.strategy = settings.STRATEGY
        self.max_total_mutations = settings.MAX_TOTAL_MUTATIONS
        self.run_lackey = settings.RUN_LACKEY
        self.server_ip = settings.SERVER_IP
        self.server_port = settings.SERVER_PORT

        if not args.no_banner:
            print(BANNER)

    def run(self):
        if self.tool == 'mutilator':
            mutilator.run(self.seed_dir, self.samples_dir,
                          self.strategy, self.max_total_mutations)

        elif self.tool == 'taskmaster':
            taskmaster.run(self.binary,
                           self.fuzz_args,
                           self.ttl,
                           self.samples_dir,
                           self.work_dir,
                           self.crash_dir,
                           self.recover_time,
                           self.destructive,
                           self.debugger)

        elif self.tool == 'autopsy':
            autopsy.run(self.binary, self.fuzz_args, self.ttl)

        elif self.tool == 'auto':

            if self.run_lackey:
                worker = Thread(target=self.lackey_worker)
                worker.start()

            worker = Thread(target=self.mutilator_worker)
            worker.start()

            taskmaster.run(self.binary,
                           self.fuzz_args,
                           self.ttl,
                           self.samples_dir,
                           self.work_dir,
                           self.crash_dir,
                           self.recover_time,
                           self.destructive,
                           self.debugger)

    def lackey_worker(self):
        # TODO: Fix the bug that this doesn't exit on KeyBoardExit.
        lackey.run(self.server_ip, self.server_port)

    def mutilator_worker(self):
        while True:
            mutilator.run(self.seed_dir, self.samples_dir,
                          self.strategy, self.max_total_mutations)
            sleep(self.recover_time)


if __name__ == '__main__':
    fizz = Fizzled()
    fizz.run()
