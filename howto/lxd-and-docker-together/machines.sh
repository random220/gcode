lxc launch ubuntu:22.04 u22lxd

cat <<'EOF' | lxc exec u22lxd bash -
hostname
apt-get -y update
apt-get -y dist-upgrade
EOF
