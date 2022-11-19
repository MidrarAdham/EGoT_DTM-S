#!/usr/bin/python3
# https://flaviocopes.com/python-http-server/
# https://pythonsansar.com/creating-simple-http-server-python/
from pathlib import Path
import sys, os
from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl
from datetime import datetime

HOST_NAME = "0.0.0.0"
PORT = 8090
LOG = ""
ROOT = ""
cwd = str(Path.cwd())
path = cwd
class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        query_pos = self.path.find('?',0,len(self.path))
        base_path = self.path[:query_pos]
        if (query_pos == -1 and base_path != '/na'):
            self.send_response(404)
            self.end_headers()
        else:
            self.send_response(201)
            self.end_headers()

            with open(LOG,'a') as file:
                content_length = int(self.headers['Content-Length'])
                file.write(self.rfile.read(content_length).decode("utf-8"))

if __name__ == "__main__":
    print('DTMC Server starting...')
    cwd = str(Path.cwd())
    LOG = cwd + datetime.now().strftime('/log_%H_%M_%d_%m_%Y.log')
    ROOT = cwd + '/build/bin'

    server = HTTPServer((HOST_NAME, PORT), handler)

    # Create an SSLContext instance by specifying the highest TLS protocol
    # that both the client and the server supports
    ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_ctx.verify_mode = ssl.CERT_REQUIRED
    ssl_ctx.check_hostname = False # If set to True, only the hostname that matches the certificate will be accepted
    ssl_ctx.hostname_checks_common_name = True
    ssl_ctx.load_verify_locations(cafile='C:/Users/sonal/Documents/GitHub/EGoT_DTM-S/doe-egot-system/src/DTM-Gen-Sim/Trust Model Classifier/client.crt')
    #ssl_ctx.get_ca_certs()
    
    ssl_ctx.load_cert_chain(certfile='C:/Users/sonal/Documents/GitHub/EGoT_DTM-S/doe-egot-system/src/DTM-Gen-Sim/Trust Model Classifier/server.crt', keyfile='C:/Users/sonal/Documents/GitHub/EGoT_DTM-S/doe-egot-system/src/DTM-Gen-Sim/Trust Model Classifier/server.key')
    server.socket = ssl_ctx.wrap_socket(
        server.socket, 
        server_side=True,
        do_handshake_on_connect=True)

    print(ssl_ctx.cert_store_stats())

    print(f"Server started http://{HOST_NAME}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print("Server stopped successfully")
        sys.exit(0)