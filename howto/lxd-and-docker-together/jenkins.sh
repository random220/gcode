#!/bin/bash

mkdir -p $HOME/J/jenkins_home
chmod 777 $HOME/J/jenkins_home
docker run -itd --name jenny -h jenny \
-p 8080:8080 -p 50000:50000 \
-v $HOME/J/jenkins_home:/var/jenkins_home jenkins/jenkins:lts-jdk11
