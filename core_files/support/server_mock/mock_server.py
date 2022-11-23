import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import socket
from threading import Thread
import requests
import json
import re
from support.constants.mocks.endpoints import PATHS


class MockServerRequestHandler(BaseHTTPRequestHandler):
    _server = None
    _thread = None

    @classmethod
    def start_mock_server(self, context, host, port):
        mock_server = HTTPServer((host, port), MockServerRequestHandler)
        context.mock_server = self._server = mock_server
        self._thread = Thread(target=context.mock_server.serve_forever)
        self._thread.setDaemon(True)
        self._thread.start()
        return context

    @staticmethod
    def get_free_port():
        s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
        s.bind(('localhost', 0))
        address, port = s.getsockname()
        s.close()
        return port

    @classmethod
    def stop_serving(self):
        # Shut down the server
        if self._server is not None:
            self._server.shutdown()

        # Let the thread rejoin the worker pool
        self._thread.join(timeout=10)
        assert not self._thread.is_alive()

    def do_GET(self):
        endpoint = os.environ['API_ENDPOINT']
        pattern = PATHS[endpoint]['PATH']
        compiled_pattern = re.compile(pattern)

        if re.search(compiled_pattern, self.path):
            # Add response status code.
            self.send_response(requests.codes.ok)

            # Get mock content.
            with open('support/constants/mocks/{}.json'.format(os.environ['API_ENDPOINT'])) as f:
                response_content = json.load(f)
                
            # Add response headers.
            self.send_header('Content-Type', 'application/json')
            self.send_header('Accept', 'application/json')
            self.send_header('Content-Length', len(json.dumps(response_content)))
            self.end_headers()

            # Encoding
            response_content = bytes(json.dumps(response_content), 'utf8')

            # Sending response
            self.wfile.write(response_content)
