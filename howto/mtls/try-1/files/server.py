import http.server
import ssl

class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
   def do_GET(self):
       # Serve a simple HTML page
       if self.path == '/':
           self.path = 'index.html'
       return super().do_GET()

def run(server_class=http.server.HTTPServer, handler_class=SimpleHTTPRequestHandler, port=4443):
   server_address = ('', port)
   httpd = server_class(server_address, handler_class)
   httpd.socket = ssl.wrap_socket(httpd.socket,
                                  keyfile='server-key.pem',
                                  certfile='server-cert.pem',
                                  server_side=True)
   print(f'Serving HTTPS on port {port}...')
   httpd.serve_forever()

if __name__ == '__main__':
   run()