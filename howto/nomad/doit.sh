# for host in nom1 nom2 nom3 nom4 nom5; do
#     (
#     multipass delete --purge $host
#     multipass launch --name $host focal
#     ) &
# done


install() {
host=$1
cat <<'EOF' | multipass exec $host bash -
cd
#curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
#sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
#sudo apt-get update && sudo apt-get install nomad
#sudo snap install docker
sudo groupadd docker
sudo usermod -aG docker ubuntu
EOF
}

for host in nom1 nom2 nom3 nom4 nom5; do
    (install $host) &
done
