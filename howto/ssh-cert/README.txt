ssh cert is all about the ssh server trusting one keypair ever
others that want to log in, must prove that they are verified by that one key pair

mkdir ~/x
cd ~/x

create that one key pair

    echo y|ssh-keygen -t rsa -b 4096 -f user_ca -C user_ca -N ''
        # user_ca
        # user_ca.pub


make the ssh server trust it

    on server as root
        cat >/etc/ssh/user_ca.pub # type the pubkey
        echo 'TrustedUserCAKeys /etc/ssh/user_ca.pub' >>/etc/ssh/sshd_config
        service ssh restart


sign the pubkey of the person who need to log in
that would be me. my pubkey ~/.ssh/id_rsa.pub

    ssh-keygen -s user_ca -I om.mandal@gmail.com-but-does-not-matter -n om,omandal -V +1d ~/.ssh/id_rsa.pub

    # this would create ~/.ssh/id_rsa-cert.pub
    # now you can delete ~/.ssh/id_rsa.pub because it's inside ~/.ssh/id_rsa-cert.pub

try login
    ssh om@the-server

----


Github specific signing
https://docs.github.com/en/enterprise-cloud@latest/organizations/managing-git-access-to-your-organizations-repositories/about-ssh-certificate-authorities

ssh-keygen -s user_ca -V '+1d' -I KEY-IDENTITY -O extension:login@github.com=omandal_pure ~/.ssh/id_rsa.pub

