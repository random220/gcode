#!/bin/bash

cat <<EOF
sudo apt-get -y install kotlin
sudo apt-get -y install default-jdk
kotlinc Main.kt -include-runtime -d Main.jar
java -jar Main.jar
EOF
