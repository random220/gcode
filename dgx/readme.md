### URLS
* https://build.nvidia.com/spark
* https://github.com/NVIDIA/dgx-spark-playbooks



### Tutes
* [Initial setup](https://docs.nvidia.com/dgx/dgx-spark/first-boot.html)
 * Connect network cable betwee DGX and router
 * Power on DGX. This will create a wifi hotspot. Connect to it from laptop. Captive portal will open a configuration page: `http://spark-e9ed.local`
     * Create Username: `zk` / `Hostart!!`
     * Once system is sshable (it would annouce itself to local dns through [mdns](https://en.wikipedia.org/wiki/Multicast_DNS)), `ssh -L 11000:localhost:11000 zk@spark-e9ed`
     * Look at DGX Dashboard: `http://localhost:11000/`
* [Connect](https://build.nvidia.com/spark/connect-to-your-spark) to your Spark. Two approaches
 * NVIDIA Sync (recommended)
 * Just SSH