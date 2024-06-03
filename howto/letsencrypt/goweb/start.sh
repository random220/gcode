#!/bin/bash

mydir=$(dirname "$(readlink -f $0)")
cd "$mydir"
if [[ ! -f serve-https ]]; then
    go build serve-https.go
fi
cd html
#go run ../serve-https.go
../serve-https
