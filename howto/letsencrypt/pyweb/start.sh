#!/bin/bash

mydir=$(dirname "$(readlink -f $0)")
cd "$mydir"/html
../serve-https.py
