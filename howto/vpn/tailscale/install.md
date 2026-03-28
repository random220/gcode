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

### DGX Spark

https://build.nvidia.com/spark/tailscale/instructions

```
# Update package list
sudo apt update

# Install required tools for adding external repositories
sudo apt install -y curl gnupg

# Add Tailscale signing key
curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/noble.noarmor.gpg | \
  sudo tee /usr/share/keyrings/tailscale-archive-keyring.gpg > /dev/null

# Add Tailscale repository
curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/noble.tailscale-keyring.list | \
  sudo tee /etc/apt/sources.list.d/tailscale.list

# Update package list with new repository
sudo apt update

# Install Tailscale
sudo apt install -y tailscale

```

Verify Tailscale installation

```
# Check Tailscale version
$ tailscale version
1.96.4
  tailscale commit: 8cf541dfd1e0a97096c01cb775d5e26336f3bc6c
  long version: 1.96.4-t8cf541dfd-g62bc84ce7
  other commit: 62bc84ce7236dafdeb40272171dae03a66502ed1
  go version: go1.26.1
```

Check Tailscale service status

```
$ sudo systemctl status tailscaled --no-pager
* tailscaled.service - Tailscale node agent
     Loaded: loaded (/usr/lib/systemd/system/tailscaled.service; enabled; preset: enabled)
     Active: active (running) since Sat 2026-03-28 12:32:34 PDT; 1min 8s ago
       Docs: https://tailscale.com/docs/
   Main PID: 9695 (tailscaled)
     Status: "Needs login: "
      Tasks: 18 (limit: 153549)
     Memory: 11.1M (peak: 13.9M)
        CPU: 108ms
     CGroup: /system.slice/tailscaled.service
             `-9695 /usr/sbin/tailscaled --state=/var/lib/tailscale/tailscaled.state --socket=/run/tailscale/tailscaled.sock --port...

Mar 28 12:32:34 tron tailscaled[9695]: Switching ipn state NoState -> NeedsLogin (WantRunning=false, nm=false)
Mar 28 12:32:34 tron tailscaled[9695]: blockEngineUpdates(true)
Mar 28 12:32:34 tron tailscaled[9695]: wgengine: Reconfig: configuring userspace WireGuard config (with 0/0 peers)
Mar 28 12:32:34 tron tailscaled[9695]: wgengine: Reconfig: configuring router
Mar 28 12:32:34 tron tailscaled[9695]: wgengine: Reconfig: user dialer
Mar 28 12:32:34 tron tailscaled[9695]: wgengine: Reconfig: configuring DNS
Mar 28 12:32:34 tron tailscaled[9695]: dns: Set: {DefaultResolvers:[] Routes:{} SearchDomains:[] Hosts:0}
Mar 28 12:32:34 tron tailscaled[9695]: dns: Resolvercfg: {Routes:{} Hosts:0 LocalDomains:[]}
Mar 28 12:32:34 tron tailscaled[9695]: dns: OScfg: {}
Mar 28 12:32:34 tron tailscaled[9695]: health(warnable=wantrunning-false): error: Tailscale is stopped.

```

Connect to Tailscale network

```
# Start Tailscale and begin authentication
sudo tailscale up

# Follow the URL displayed to complete login in your browser
# Choose from: Google, GitHub, Microsoft, or other supported providers

```


