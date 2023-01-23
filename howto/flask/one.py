#!/usr/bin/env python3

from flask import Flask, escape
import sys

app = Flask(__name__)

@app.route("/")
def display_om():
    with open(sys.argv[0]) as file:
        contents = file.read()
    contents = str(escape(contents))
    return f"<pre>{contents}</pre>"

if __name__ == "__main__":
    app.run()

