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
