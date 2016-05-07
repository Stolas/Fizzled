#!/usr/bin/env python
import logging
from datetime import datetime
from json import dumps as json_encode
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

logger = logging.getLogger('lackey')

class LackeyHandler(BaseHTTPRequestHandler):
    def do_GET(sender):
        sender.send_response(200)
        sender.send_header('Content-Type', 'application/json')
        sender.end_headers()

        data = dict()

        data['time'] = dict()
        now = datetime.now()
        data['time']['year'] = now.year
        data['time']['month'] = now.month
        data['time']['day'] = now.day
        data['time']['hour'] = now.hour
        data['time']['minute'] = now.minute
        data['time']['second'] = now.second

        # TODO: Return file counts of folders.
        # TODO: Create a call to read files.
        # TODO: Add SSL
        # TODO: Add Authentication Tokens

        sender.wfile.write(json_encode(data))

class Lackey():
    def __init__(self,hostname, port, seed_dir, samples_dir, crash_dir):
        logger.info('Lackey listening at {}:{}'.format(hostname, port))
        self.httpd = HTTPServer((hostname, port), LackeyHandler)
        self.seed_dir = seed_dir
        self.samples_dir = samples_dir
        self.crash_dir = crash_dir

    def run(self):
        # TODO: Set logger for httpd
        self.httpd.serve_forever()
        logger.debug('Lackey shutdown at {}:{}')

    def exit(self):
        self.httpd.server_close()