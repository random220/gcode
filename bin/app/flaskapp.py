#!/usr/bin/env python3

from flask import Flask, request, render_template_string, send_from_directory
import os

app = Flask(__name__)
BASE_DIR = os.getcwd()  # Use the current working directory as the base directory

@app.route('/')
@app.route('/<path:subpath>', methods=['GET', 'POST'])
def browse_files(subpath=''):
    full_path = os.path.abspath(os.path.join(BASE_DIR, subpath))
    if not full_path.startswith(BASE_DIR):
        return 'Invalid path', 400

    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            filepath = os.path.join(full_path, file.filename)
            file.save(filepath)
            return f'File successfully uploaded to {filepath}'

    if os.path.isdir(full_path):
        files = sorted(os.listdir(full_path), key=lambda s: s.lower())
        file_list_html = ''.join([
            f'<li><a href="/{os.path.join(subpath, file)}" style="{"background-color: lightgreen;" if os.path.isdir(os.path.join(full_path, file)) else ""}">{file}</a></li>'
            for file in files
        ])
        return f'''
        <!doctype html>
        <title>File Browser</title>
        <h1>Files in {subpath or 'root'}</h1>
        <form method="post" enctype="multipart/form-data">
          <input type="file" name="file">
          <input type="submit" value="Upload">
        </form>
        <ul>
        {file_list_html}
        </ul>
        '''
    elif os.path.isfile(full_path):
        file_ext = os.path.splitext(full_path)[1].lower()
        if file_ext in ['.pdf', '.png', '.jpg', '.jpeg', '.mp3', '.mp4', '.html']:
            return send_from_directory(BASE_DIR, os.path.join(subpath))
        else:
            with open(full_path, 'r') as f:
                content = f.read()
            return f'''
            <!doctype html>
            <title>View File</title>
            <h1>{subpath}</h1>
            <pre>{content}</pre>
            <a href="/">Back</a>
            '''
    else:
        return 'File not found', 404

if __name__ == '__main__':
    app.run(debug=True)
