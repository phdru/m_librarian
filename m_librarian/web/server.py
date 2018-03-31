from bottle import run

from wsgiref import simple_server
from wsgiref.handlers import SimpleHandler
from wsgiref.simple_server import WSGIServer
from bottle import route

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
    run(host=host, port=port, server_class=QuitWSGIServer, debug=True)
