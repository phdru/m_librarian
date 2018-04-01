import os
import sys
from wsgiref import simple_server
from wsgiref.handlers import SimpleHandler
from wsgiref.simple_server import WSGIServer

from bottle import route, run

simple_server.ServerHandler = SimpleHandler  # Stop logging to stdout


class QuitWSGIServer(WSGIServer):
    _quit_flag = False

    def serve_forever(self):
        while not self._quit_flag:
            self.handle_request()


@route('/quit')
def quit():
    QuitWSGIServer._quit_flag = True
    return "The program has finished. Have a nice day!"


def run_server(host='localhost', port=0):
    # Start here so that bottle can find templates
    os.chdir(os.path.dirname(__file__))
    sys.path.insert(0, os.getcwd())  # To import Cheetah templates
    run(host=host, port=port, server_class=QuitWSGIServer, debug=True)
