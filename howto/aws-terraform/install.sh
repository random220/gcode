#!/bin/bash

apt-get -y update
apt-get -y dist-upgrade
apt-get -y install sudo vim git curl openssh-client python3
apt-get -y install zip unzip tmux file netcat # useful utils

mkdir /tmp/a
cd /tmp/a

curl -o a.zip "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip"
mkdir a
(
cd a
unzip ../a.zip
sudo ./aws/install
)
rm -rf a.zip a

curl -o a.zip "https://releases.hashicorp.com/terraform/1.5.1/terraform_1.5.1_linux_amd64.zip"
mkdir a
(
cd a
unzip ../a.zip
sudo mv terraform /usr/local/bin
)
rm -rf a.zip a


apt-get -y install mandoc # needed for "aws help" command
apt-get -y install jq     # needed for json manipulation

useradd -s /bin/bash -m om
echo 'om ALL=(ALL:ALL) NOPASSWD: ALL' >/etc/sudoers.d/om