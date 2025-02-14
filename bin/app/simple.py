#!/usr/bin/env python3

import http.server
import socketserver
import os
import io  # Add this import

print('/?authuser=0\n\n')

PORT = 8001
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        boundary = self.headers['Content-Type'].split('=')[1].encode()
        parts = body.split(boundary)

        for part in parts:
            if b'filename="' in part:
                filename = part.split(b'filename="')[1].split(b'"')[0].decode()
                file_data = part.split(b'\r\n\r\n')[1].rsplit(b'\r\n', 1)[0]
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                with open(filepath, 'wb') as f:
                    f.write(file_data)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'File successfully uploaded to ' + filepath.encode())
                return

        self.send_response(400)
        self.end_headers()
        self.wfile.write(b'Failed to upload file')

    def list_directory(self, path):
        try:
            file_list = os.listdir(path)
        except OSError:
            self.send_error(404, "No permission to list directory")
            return None
        file_list.sort(key=lambda a: a.lower())
        displaypath = os.path.relpath(path, os.getcwd())
        r = []
        r.append('<!DOCTYPE html>')
        r.append('<html><head><title>Directory listing for %s</title></head>' % displaypath)
        r.append('<body><h2>Directory listing for %s</h2>' % displaypath)
        r.append('<hr><ul>')
        for name in file_list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            r.append('<li><a href="%s">%s</a></li>' % (linkname, displayname))
        r.append('</ul><hr>')
        r.append('''
        <h2>Upload File</h2>
        <form method="post" enctype="multipart/form-data">
          <input type="file" name="file">
          <input type="submit" value="Upload">
        </form>
        ''')
        r.append('</body></html>')
        encoded = '\n'.join(r).encode('utf-8', 'surrogateescape')
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return f

    def do_GET(self):
        if self.path == '/':
            self.path = UPLOAD_FOLDER
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()

