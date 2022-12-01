
cat '/Library/Preferences/VMware Fusion/vmnet2/dhcpd.conf' >a.txt
cat <<'EOF' >>a.txt
host noms1 {
    hardware ethernet 00:50:56:3E:0C:FA;
    fixed-address 10.32.32.128;
}
host noms2 {
    hardware ethernet 00:50:56:3E:A7:10;
    fixed-address 10.32.32.129;
}
host noms3 {
    hardware ethernet 00:50:56:2C:20:42;
    fixed-address 10.32.32.130;
}
EOF

cat a.txt | sudo tee '/Library/Preferences/VMware Fusion/vmnet2/dhcpd.conf'

--------------------------------------------------------

s1=10.32.32.128
s2=10.32.32.129
s3=10.32.32.130
x=s3

ssh om@$(eval echo '$'$x)

sudo perl -i -pe "s/nom0/nom$x/" /etc/hosts /etc/hostname
sudo reboot

ssh om@$x

sudo systemctl stop nomad
sudo chown -R root:root /etc/nomad.d
sudo chmod -R a+rX /etc/nomad.d
cat /etc/nomad.d/client.hcl|sed 's/^/#/' >a.txt
cat a.txt | sudo tee /etc/nomad.d/client.hcl >/dev/null
rm a.txt
sudo bash -c 'rm -rf /opt/nomad/*'
sudo shutdown -h now

