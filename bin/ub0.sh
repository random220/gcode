cat <<EOF | sudo su -c bash -
apt-get -y install tmux vim wget curl git rsync zip unzip jq
apt-get -y install iproute2 inetutils-ping
apt-get -y install perl make gcc
apt-get -y install sqlite3
apt-get -y install python3
apt-get -y install python3-pip

apt-get -y install podman-docker

apt-get -y install squid
# mv /etc/squid/squid.conf /etc/squid/squid.conf.0
# egrep -v '^\#|^$' /etc/squid/squid.conf.0 >/etc/squid/squid.conf
# echo 'acl all src 0.0.0.0/0' >>/etc/squid/squid.conf
# echo 'http_access allow all' >>/etc/squid/squid.conf
# service squid restart

EOF

# https://www.redhat.com/sysadmin/rootless-podman-user-namespace-modes
mkdir -p ~/.config/containers

cat <<EOF >~/.config/containers/containers.conf
[containers]
userns = "nomap"
EOF

