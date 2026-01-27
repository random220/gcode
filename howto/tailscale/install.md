### Mac


- Install GO from [https://go.dev/dl/](https://go.dev/dl/) using the appropriate package

 ```
mkdir -p ~/sb
cd ~/sb
git clone https://github.com/tailscale/tailscale.git
cd tailscale
go install tailscale.com/cmd/tailscale{,d}
sudo $HOME/go/bin/tailscaled install-system-daemon
~/go/bin/tailscale up
```

### Linux

```
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```





