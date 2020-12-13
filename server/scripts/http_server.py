from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from postgres_adapter import Database
import json
import time

db = Database()

def Post_to_db(data):
    if db.connect() == 0:
        logging.info('POST connect to db')
        db.insert_player(tuple(data.values()))
        db.close_db_connection()       

def Get_from_db(id):
    if db.connect() == 0:
        logging.info('GET connect to db')
        player_data = db.read_player(id)
        db.close_db_connection() 
        return player_data

class Server(BaseHTTPRequestHandler):

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        player_record = Get_from_db(int(self.path.replace("/","")))
        self.wfile.write(str(player_record).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), post_data.decode('utf-8'))
        player_record = json.loads(post_data.decode('utf-8'))
        Post_to_db(player_record)
        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=Server, port=8000):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    time.sleep(10)
    if db.connect() == 0:
        db.create_table_players("players")
        db.close_db_connection()
    else:
        logging.error('Cannot connect to db')
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
