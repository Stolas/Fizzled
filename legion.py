#!/usr/bin/env python

import logging

# TODO: Move this to a config file.
# So I can easily log to the centralized server.
logger = logging.getLogger('legion')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

def run(data_dir, file_type):
    logger.fatal("Not yet implemented.")
    # Crawl the internet for the required filetype.
    # Fetch as many as it can


if __name__ == '__main__':
    DATA_DIRECTORY = 'data'
    FILE_TYPE = 'pdf'
    run(DATA_DIRECTORY, FILE_TYPE)
