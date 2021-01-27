#!/bin/bash

ssh-keygen -f id_rsa.pub -e -m PKCS8 > id_rsa.pub.pem
openssl rsautl -encrypt -oaep -pubin -inkey id_rsa.pub.pem -in message.txt -out message.txt.enc
rm -f id_rsa.pub.pem
