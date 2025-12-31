### URLS
* [https://build.nvidia.com/spark](https://build.nvidia.com/spark)
* [https://github.com/NVIDIA/dgx-spark-playbooks](https://github.com/NVIDIA/dgx-spark-playbooks)



### Tutes
* [Initial setup](https://docs.nvidia.com/dgx/dgx-spark/first-boot.html)
 * Connect network cable betwee DGX and router
 * Power on DGX. This will create a wifi hotspot. Connect to it from laptop. Captive portal will open a configuration page: `http://spark-e9ed.local`
     * Create Username: `zk` / `Hostart!!`
     * Once system is sshable (it would annouce itself to local dns through [mdns](https://en.wikipedia.org/wiki/Multicast_DNS)), `ssh -L 11000:localhost:11000 zk@spark-e9ed`
     * Look at DGX Dashboard: `http://localhost:11000/`
* **[Connect](https://build.nvidia.com/spark/connect-to-your-spark) to your Spark. Two approaches**
 * NVIDIA Sync (recommended)
 * Just SSH
* **[Open WebUI](https://build.nvidia.com/spark/open-webui/sync) for running Ollama server**
 * `docker pull ghcr.io/open-webui/open-webui:ollama`
* **Activating wifi afterwards**
 * `nmcli device wifi list`

     ```
$ nmcli device wifi list
IN-USE  BSSID              SSID              MODE   CHAN  RATE        SIGNAL  BARS  SECURITY
        C0:A0:0D:2F:3B:90  crondite2         Infra  1     195 Mbit/s  100     ****  WPA2
        C6:A0:0D:2F:3B:93  crondite2         Infra  149   540 Mbit/s  100     ****  WPA2
        C0:A0:0D:2F:3B:93  --                Infra  149   540 Mbit/s  100     ****  WPA2
        08:B4:B1:8E:0D:6D  google-cron       Infra  11    130 Mbit/s  92      ****  WPA2
        08:B4:B1:8E:0D:69  google-cron       Infra  149   270 Mbit/s  69      ***   WPA2
        08:B4:B1:8F:31:03  google-cron       Infra  6     130 Mbit/s  64      ***   WPA2
        98:ED:5C:8C:BA:D3  TeslaPV_8CBAD3    Infra  11    54 Mbit/s   64      ***   WPA2
        08:B4:B1:8D:ED:1D  google-cron       Infra  1     130 Mbit/s  54      **    WPA2
        DC:8D:8A:14:E1:C4  ATTZIUcIPu        Infra  8     260 Mbit/s  49      **    WPA2
        6C:5A:B0:6D:F6:5C  ATTZIUcIPu_EXT    Infra  8     130 Mbit/s  39      **    WPA2
        DC:8D:8A:14:E1:C8  ATTZIUcIPu        Infra  48    540 Mbit/s  30      *     WPA2
        DC:8D:8A:14:E1:CC  ATTZIUcIPu        Infra  100   540 Mbit/s  29      *     WPA2
        DC:8D:8A:14:E1:CF  --                Infra  100   540 Mbit/s  29      *     WPA2
        08:B4:B1:8F:30:FF  google-cron       Infra  149   270 Mbit/s  27      *     WPA2
        08:B4:B1:8D:ED:19  google-cron       Infra  149   270 Mbit/s  25      *     WPA2
        0A:B4:B1:8E:0D:69  508CE5BF          Mesh   149   270 Mbit/s  25      *     WPA3
        D0:FC:D0:0D:5F:05  ATTHzSjstA_Guest  Infra  6     260 Mbit/s  22      *     WPA2
        3E:2D:9E:8F:3D:4D  Standa            Infra  11    540 Mbit/s  22      *     WPA2 WPA3
        D0:FC:D0:0D:5F:04  ATTEllieHouse     Infra  6     260 Mbit/s  20      *     WPA2
        3E:2D:9E:8F:3D:4A  --                Infra  11    540 Mbit/s  20      *     WPA2 802.1X
        3E:2D:9E:8C:D6:15  omid              Infra  6     540 Mbit/s  17      *     WPA2 WPA3
        3E:2D:9E:8C:D6:12  --                Infra  6     540 Mbit/s  15      *     WPA2 802.1X
        3E:2D:9E:8C:D6:16  --                Infra  6     540 Mbit/s  15      *     WPA2
        2C:B8:ED:33:AF:D5  SVA               Infra  6     195 Mbit/s  15      *     WPA2
        28:BD:89:D2:BA:23  hackers           Infra  11    130 Mbit/s  14      *     WPA2
        FA:D2:AC:B4:F2:BA  --                Infra  6     540 Mbit/s  12      *     WPA2 802.1X
        FA:D2:AC:B4:F2:BB  --                Infra  6     540 Mbit/s  12      *     WPA2
        30:23:03:4D:C2:94  Wemo.Mini.1D0     Infra  6     135 Mbit/s  12      *     --
        24:A2:E1:EE:85:28  standa            Infra  11    195 Mbit/s  12      *     WPA2
     ```
  * `nmcli device wifi connect <SSID> password <WiFi_Password>`

     ```
     $ sudo nmcli device wifi connect 'C6:A0:0D:2F:3B:93' password OUR-WIFI-PASS

     Device 'wlP9s9' successfully activated with 'ff137d9e-2c0b-4993-b783-5edfc89792f4'.

     $ ip a|grep 192.168
     inet 192.168.10.196/24 brd 192.168.10.255 scope global dynamic noprefixroute enP7s7
     inet 192.168.10.178/24 brd 192.168.10.255 scope global dynamic noprefixroute wlP9s9

     $ nmcli connection show
NAME                UUID                                  TYPE      DEVICE
crondite2           ff137d9e-2c0b-4993-b783-5edfc89792f4  wifi      wlP9s9
lo                  a87e48af-930a-41a1-b768-3216e97e87cb  loopback  lo
br-9a8ba5756691     f5485fd1-7fbc-4e16-849a-31394e85000f  bridge    br-9a8ba5756691
docker0             b3feba1e-826a-4fa1-9c43-76b89f2ef4c1  bridge    docker0
mpqemubr0           86114134-7d0c-40b1-83a7-2ee562375aaa  bridge    mpqemubr0
Wired connection 1  9ff28182-6215-3223-a210-cc2e54d621a5  ethernet  --
Wired connection 2  ba52e567-165f-3b8e-83e4-9ccfa39c2e42  ethernet  --
Wired connection 3  4f0275e3-597f-3e24-a60c-55851cce7f0d  ethernet  --
Wired connection 4  197c6c5e-c0dd-32af-9746-4484724d30c4  ethernet  --
Wired connection 5  543b2331-3c13-306e-8414-5e30a11938e5  ethernet  --

     ```

---

## Connecting to Wi-Fi Using nmcli

nmcli is a command-line tool for managing network connections on Linux systems. It is part of the NetworkManager suite and allows users to create, display, edit, delete, enable, and disable network connections, as well as control and display network device status.

### Step-by-Step Guide to Connect to Wi-Fi

#### Step 1: Enable Your Wi-Fi Device

First, ensure that your Wi-Fi device is enabled. You can check the status of all network interfaces with:

```
nmcli dev status
```

To specifically check if Wi-Fi is enabled, use:

```
nmcli radio wifi
```

If Wi-Fi is disabled, enable it with:

```
nmcli radio wifi on
```

#### Step 2: Identify a Wi-Fi Access Point

To find available Wi-Fi networks, scan for nearby networks:

```
nmcli dev wifi list
```

Note the SSID (name) of the network you want to connect to.

#### Step 3: Connect to Wi-Fi

With Wi-Fi enabled and the SSID identified, connect to the network using:

```
sudo nmcli dev wifi connect network-ssid
```

Replace network-ssid with the name of your network. If the network requires a password, include it in the command:

```
sudo nmcli dev wifi connect network-ssid password "network-password"
```

Alternatively, to avoid displaying the password on the screen, use the --ask option:

```
sudo nmcli --ask dev wifi connect network-ssid
```

This will prompt you to enter the network password securely.

#### Verify Connection

To verify that you are connected to the internet, you can use the ping command:

```
ping google.com
```

#### Managing Network Connections

To view all saved connections, use:

```
nmcli con show
```

To disconnect from a network, specify the SSID or UUID:

```
nmcli con down ssid/uuid
```

To connect to another saved network, use:

```
nmcli con up ssid/uuid
```

### Docker setup
 - Ref: [https://docs.nvidia.com/dgx/dgx-spark/nvidia-container-runtime-for-docker.html](https://docs.nvidia.com/dgx/dgx-spark/nvidia-container-runtime-for-docker.html)
 - Apparently `--runtime=nvidia` is no longer required
 - check GPU availability from inside container

 ```
 nvidia-smi >~/a.txt
 docker run -it --gpus=all nvcr.io/nvidia/cuda:13.0.1-devel-ubuntu24.04 nvidia-smi >~/b.txt
 vimdiff ~/a.txt ~/b.txt
 ```
 - Another way

 ```
 % docker run -itd --name cuds -h cuds \
 --gpus=all nvcr.io/nvidia/cuda:13.0.1-devel-ubuntu24.04 bash
 % docker exec -it cuds bash

 root@cuds:~# ls -ld /dev/nvidia*
 crw-rw-rw- 1 root root 500,   0 Dec 28 05:35 /dev/nvidia-uvm
 crw-rw-rw- 1 root root 500,   1 Dec 28 05:35 /dev/nvidia-uvm-tools
 crw-rw-rw- 1 root root 195,   0 Dec 28 05:35 /dev/nvidia0
 crw-rw-rw- 1 root root 195, 255 Dec 28 05:35 /dev/nvidiactl
 ```
 - [NGC](https://docs.nvidia.com/dgx/dgx-spark/ngc.html) (docker registry for GPU optimized containers)
   - [https://catalog.ngc.nvidia.com/](https://catalog.ngc.nvidia.com/)
     - Account info (passwd host)

       ```
       cat <<EOF >a.txt.gpg.txt
       -----BEGIN PGP MESSAGE-----
       jA0ECQMIH7EGGh2Ta23/0sCNAVHZq4LZ8WpjbDChQ/Muq+kVI7+m/uavXMWU0CM6
       mJkCewoLFxhyxxQhiR2WVlUUTs/pWZ0ySrEIs0c2u+LauuVxorPlxGK6SOOLjATe
       IAbJkW8q5eWpp8peEz3RV5J65FZEG9M73G2j/7k5lbJ5zUQSWh4WSzX6OWGRNYGY
       BPUWjOjuZO3p9P+5aREJdGvd/x5f1ZlHSnaZAENGy0W+pyKXyRECxzRT8spzYKSx
       hs5S4ZupLpZ1z4SyGiP8vQvmvVSMVnzfraGpA7gfTMq3UNGYjzw56x4FX/Wrtipp
       vbwOivfBs7B7pUGKgrkh5cGxYDdwOjL5EJFBm3CfDw1asSvW5Tsvv6LkzNk01Hwd
       su/fkUhOC7MJ+NpvT1p3VI3+7cfl6SImkcckh8Msf7qC0kje8GApVAPm15vIJXzC
       NLQS9g1zjErtXMsXjd58
       =ur4R
       -----END PGP MESSAGE-----
       EOF
       ```

     - Actual [catalog](https://build.nvidia.com/explore/discover)
     - Get [CLI installer](https://org.ngc.nvidia.com/setup/installers/cli)
     - Be sure to get ARM64 Linux version of CLI.
       With NVIDIA GPU Cloud (NGC) CLI, you can perform many of the
       same operations that are available from the NGC website, such
       as running jobs, viewing Docker repositories and downloading
       AI models within your organization and team space.
     - `docker login -u '$oauthtoken' nvcr.io` And then paste the token
     - `docker logout; rm -f ~/.docker/config.json`


### Image generation (Comfy UI)
- [https://build.nvidia.com/spark/comfy-ui](https://build.nvidia.com/spark/comfy-ui)
- Steps

  ```
  ssh om@tron
  mkdir -p ~/sb/comfy
  cd ~/sb/comfy
  python3 -m venv e
  . e/bin/activate
  pip install -U pip
  pip3 install -U torch torchvision --index-url https://download.pytorch.org/whl/cu130
  git clone https://github.com/comfyanonymous/ComfyUI.git
  cd ComfyUI/
  pip install -U -r requirements.txt

  cd models/checkpoints/
  wget https://huggingface.co/Comfy-Org/stable-diffusion-v1-5-archive/resolve/main/v1-5-pruned-emaonly-fp16.safetensors
  cd ../../

  # Run server
  python main.py --listen 0.0.0.0

  # Verify running
  $ curl -I http://localhost:8188

  HTTP/1.1 200 OK
  Cache-Control: no-cache
  Pragma: no-cache
  Expires: 0
  Content-Type: text/html
  Etag: "188580056defed42-53e"
  Last-Modified: Sun, 28 Dec 2025 21:59:50 GMT
  Content-Length: 1342
  Accept-Ranges: bytes
  Date: Sun, 28 Dec 2025 22:08:10 GMT
  Server: Python/3.13 aiohttp/3.13.2
  ```
- First generation [https://docs.comfy.org/get_started/first_generation](https://docs.comfy.org/get_started/first_generation)

```

```

### Vibe Coding
URL: [https://build.nvidia.com/spark/vibe-coding](https://build.nvidia.com/spark/vibe-coding)

```
ssh ztron

# Install ollama

zk@tron:~$ curl -fsSL https://ollama.com/install.sh | sh
>>> Installing ollama to /usr/local
[sudo] password for zk:
>>> Downloading Linux arm64 bundle
######################################################################## 100.0%
>>> Creating ollama user...
>>> Adding ollama user to render group...
>>> Adding ollama user to video group...
>>> Adding current user to ollama group...
>>> Creating ollama systemd service...
WARNING: systemd is not running
>>> NVIDIA GPU installed.
>>> The Ollama API is now available at 127.0.0.1:11434.
>>> Install complete. Run "ollama" from the command line.
zk@tron:~$

$ ollama serve # needed because ollama service is not running. the systemd warning??

$ ollama pull gpt-oss:120b # took an hour



```


