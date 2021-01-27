#!/bin/bash

cp id_rsa idrsa
chmod 600 idrsa
ssh-keygen -p -m PEM -N '' -f idrsa
openssl rsautl -decrypt -oaep -inkey idrsa <message.txt.enc >message.txt.dec
rm -f idrsa
