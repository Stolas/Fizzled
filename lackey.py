#!/usr/bin/env python
import logging
from json import dumps as json_encode
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

logger = logging.getLogger('lackey')

class LackeyHandler(BaseHTTPRequestHandler):
    def do_GET(sender):
        sender.send_response(200)
        sender.send_header('Content-Type', 'application/json')
        sender.end_headers()

        data = {'status': 'TODO'}
        sender.wfile.write(json_encode(data))

def run(hostname, port):
    logger.info('Lackey listening at {}:{}'.format(hostname, port))
    httpd = HTTPServer((hostname, port), LackeyHandler)
    try:
        # TODO: Set logger for httpd
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logger.debug('Lackey shutdown at {}:{}')

if __name__ == '__main__':
    from settings import *
    ret = run(SERVER_IP, SERVER_PORT)
    sys.exit(ret)
