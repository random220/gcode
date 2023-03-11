mkdir ~/x
chmod 700 ~/x
cd ~/x

# Certificate Authority
echo y|ssh-keygen -t rsa -b 4096 -f user_ca -C user_ca -N ''
    # user_ca
    # user_ca.pub


echo y|ssh-keygen -f user-key -b 4096 -t rsa -N ''

ssh-keygen -s user_ca -I om.mandal@gmail.com -n om,omandal -V +1d user-key.pub

scp user_ca.pub om@vpn:.
ssh vpn
sudo mv user_ca.pub /etc/ssh
sudo bash -c "echo 'TrustedUserCAKeys /etc/ssh/user_ca.pub' >>/etc/ssh/sshd_config"
sudo service ssh restart
sudo useradd -s /bin/bash -m omandal
ssh -i ~/x/user-key omandal@vpn

yee!
