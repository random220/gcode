#!/bin/bash

mkdir -p $HOME/J/jenkins_home
chmod 777 $HOME/J/jenkins_home
docker run -itd --name jenny -h jenny \
--restart=on-failure \
-p 8080:8080 -p 50000:50000 \
-v $HOME/J/jenkins_home:/var/jenkins_home jenkins/jenkins:lts-jdk11


#http://gaia:8080/cli/

curl -sL -O http://gaia:8080/jnlpJars/jenkins-cli.jar
mkdir -p ~/bin
mv jenkins-cli.jar ~/bin

# generate a token from http://gaia:8080/user/ir/configure
# keep in ~/.ssh/token-gaia as ir:token

alias jc="java -jar $HOME/bin/jenkins-cli.jar -auth @$HOME/.ssh/token-gaia -s http://gaia:8080/ -webSocket"

