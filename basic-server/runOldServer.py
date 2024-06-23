import logging
import sys
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from ScoreManager import ScoreManager

PORT = 8000

SM = ScoreManager()

class basicResponseHandler(BaseHTTPRequestHandler):

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run():
    logging.basicConfig(level=logging.INFO)
    SM = ScoreManager()
    logging.info('Score Manager init \n')
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, basicResponseHandler)
    logging.info('Starting server...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping server\n')

if __name__ == '__main__':
    run()