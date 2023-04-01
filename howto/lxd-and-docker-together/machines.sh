#!/bin/bash

lxc launch ubuntu:22.04 u22lxd

cat <<'EOF' | lxc exec u22lxd bash -
apt-get -y update
apt-get -y dist-upgrade
apt-get -y autoremove

apt-get -y install vim tmux git 
EOF

lxc stop u22lxd
lxc snapshot u22lxd
lxc copy u22lxd/snap0 java11
lxc start java11

cat <<'EOF' | lxc exec java11 bash -
apt-get -y update
apt-get -y install openjdk-11-jdk-headless
useradd -s /bin/bash -m ir
echo 'ir:welcome'|chpasswd
umask 077
mkdir ~ir/.ssh
ssh-keygen -t ed25519 -f ~ir/.ssh/id_ed25519 -N ''
chown -R ir:ir ~ir/.ssh
echo 'ir ALL=(ALL:ALL) NOPASSWD: ALL' >/etc/sudoers.d/ir
perl -i -pe 's/^PasswordAuthentication.*/PasswordAuthentication yes\n/s' /etc/ssh/sshd_config
EOF

lxc stop java11
lxc snapshot java11

lxc cp java11/snap0 cl0
lxc cp java11/snap0 cl1
lxc cp java11/snap0 cl2
lxc cp java11/snap0 cl3
lxc cp java11/snap0 cl4
lxc cp java11/snap0 cl5
lxc cp java11/snap0 cl6
lxc cp java11/snap0 cl7
lxc cp java11/snap0 cl8
lxc cp java11/snap0 cl9
lxc start cl0 cl1 cl2 cl3 cl4 cl5 cl6 cl7 cl8 cl9

mkdir -p $HOME/J/jenkins_home
chmod 777 $HOME/J/jenkins_home
docker run -itd --name jenny -h jenny \
-p 8080:8080 -p 50000:50000 \
-v $HOME/J/jenkins_home:/var/jenkins_home jenkins/jenkins:lts-jdk11


