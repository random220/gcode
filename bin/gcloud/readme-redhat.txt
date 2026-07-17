
git clone https://github.com/rofl0r/microsocks.git
cd microsocks
make
mkdir -p ~/bin
mv microsocks ~/bin


$ sudo firewall-cmd --add-port=8484/tcp --permanent
$ sudo firewall-cmd --reload
