cat <<EOF | sudo su -c bash -
apt-get -y install tmux vim wget curl git rsync zip unzip jq
apt-get -y install iproute2 inetutils-ping
apt-get -y install perl make gcc
apt-get -y install sqlite3
apt-get -y install python3
apt-get -y install python3-pip

apt-get -y install podman-docker
EOF

# https://www.redhat.com/sysadmin/rootless-podman-user-namespace-modes
mkdir -p ~/.config/containers

cat <<EOF >~/.config/containers/containers.conf
[containers]
userns = "nomap"
EOF

