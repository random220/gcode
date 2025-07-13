#!/bin/bash
cat <<EOF
sudo apt-get -y install scala
sudo apt-get -y install default-jdk
scalac Main.scala
scala Main
EOF
