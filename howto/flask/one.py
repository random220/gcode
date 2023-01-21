#!/usr/bin/env python3

from flask import Flask, escape

app = Flask(__name__)

@app.route("/")
def display_file():
    with open("/Users/om/a.txt") as file:
        contents = file.read()
    #return "<pre>" + escape(contents) + "</pre>"
    return "<pre>" + contents + "</pre>"

if __name__ == "__main__":
    app.run()
