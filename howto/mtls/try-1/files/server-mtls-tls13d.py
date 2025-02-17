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
    
    # Create an SSL context with the latest protocols
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    
    # Load server certificate and key
    context.load_cert_chain(certfile='server-cert.pem', keyfile='server-key.pem')
    
    # Load CA certificate to verify client certificates
    context.load_verify_locations(cafile='ca-cert.pem')
    context.verify_mode = ssl.CERT_REQUIRED  # Require client certificate
    
    # Apply the SSL context to the server socket
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    
    print(f'Serving HTTPS on port {port} with TLS 1.3 only...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
