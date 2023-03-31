#!/bin/bash

#https://discuss.linuxcontainers.org/t/lxd-and-docker-firewall-redux-how-to-deal-with-forward-policy-set-to-drop/9953/3?u=tomp
#sudo iptables -I DOCKER-USER  -j ACCEPT

mydir=$(cd "$(dirname $0)" && pwd -P)
"$mydir/docki22"


