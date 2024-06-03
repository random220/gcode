#!/usr/bin/env python3

import http.server
import ssl
import os

port = 4343
server_address = ('localhost', port)
httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain('../certs/fullchain.pem', '../certs/privkey.pem')

httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)

cwd = os.getcwd()
print('----------------------------------------------')
print(f"HTTPS server running on port {port}")
print(f"Serving files from {cwd}")
print('----------------------------------------------')

httpd.serve_forever()
