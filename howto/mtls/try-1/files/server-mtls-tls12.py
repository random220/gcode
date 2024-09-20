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
    
    # Create an SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(certfile='server-cert.pem', keyfile='server-key.pem')
    context.load_verify_locations(cafile='ca-cert.pem')
    context.verify_mode = ssl.CERT_REQUIRED  # Require client certificate

    # Apply the SSL context to the server socket
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    
    print(f'Serving HTTPS on port {port} with TLS 1.2 only...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
