#!/bin/bash
sudo snap remove lxd
sudo apt-get -y install bridge-utils
sudo ip link set lxdbr0 down
sudo brctl delbr lxdbr0
sudo snap install lxd
sudo usermod -aG lxd $USER


#sudo lxd init --auto --storage-backend=zfs --storage-create-device=/dev/sdb
sudo lxd init --auto --storage-backend=zfs --storage-create-loop=60




#    ---------------------------------------------------------------------------------------------------------
#    
#    sudo lxd init --minimal
#    # % lxc storage list
#    # To start your first container, try: lxc launch ubuntu:22.04
#    # Or for a virtual machine: lxc launch ubuntu:22.04 --vm
#    # 
#    # +---------+--------+------------------------------------------------+-------------+---------+---------+
#    # |  NAME   | DRIVER |                     SOURCE                     | DESCRIPTION | USED BY |  STATE  |
#    # +---------+--------+------------------------------------------------+-------------+---------+---------+
#    # | default | dir    | /var/snap/lxd/common/lxd/storage-pools/default |             | 1       | CREATED |
#    # +---------+--------+------------------------------------------------+-------------+---------+---------+
#    
#    # http://www.panticz.de/lxd/storage
#    sudo fallocate -l 60G /b/myzpool-60gb.disk
#    sudo apt-get -y install zfsutils-linux
#    sudo zpool create myzpool-60gb /b/myzpool-60gb.disk
#    # % sudo zpool list
#    # NAME           SIZE  ALLOC   FREE  CKPOINT  EXPANDSZ   FRAG    CAP  DEDUP    HEALTH  ALTROOT
#    # myzpool-60gb  59.5G   100K  59.5G        -         -     0%     0%  1.00x    ONLINE  -
#    
#    lxc storage create mylxpool-60gb zfs source=myzpool-60gb
#    # % lxc storage list
#    # +---------------+--------+------------------------------------------------+-------------+---------+---------+
#    # |     NAME      | DRIVER |                     SOURCE                     | DESCRIPTION | USED BY |  STATE  |
#    # +---------------+--------+------------------------------------------------+-------------+---------+---------+
#    # | default       | dir    | /var/snap/lxd/common/lxd/storage-pools/default |             | 1       | CREATED |
#    # +---------------+--------+------------------------------------------------+-------------+---------+---------+
#    # | mylxpool-60gb | zfs    | myzpool-60gb                                   |             | 0       | CREATED |
#    # +---------------+--------+------------------------------------------------+-------------+---------+---------+
#    
#    # % lxc profile show default
#    # config: {}
#    # description: Default LXD profile
#    # devices:
#    #   eth0:
#    #     name: eth0
#    #     network: lxdbr0
#    #     type: nic
#    #   root:
#    #     path: /
#    #     pool: default
#    #     type: disk
#    # name: default
#    # used_by: []
#    # 
#    
#    # % lxc profile device list default
#    # root
#    # eth0
#    
#    lxc profile device remove default root
#    # Device root removed from default
#    
#    lxc profile device add default root disk path=/ pool=mylxpool-60gb
#    # Device root added to default
#    
#    # % lxc profile show default
#    # config: {}
#    # description: Default LXD profile
#    # devices:
#    #   eth0:
#    #     name: eth0
#    #     network: lxdbr0
#    #     type: nic
#    #   root:
#    #     path: /
#    #     pool: mylxpool-60gb
#    #     type: disk
#    # name: default
#    # used_by: []
#    
#    
#    lxc storage delete default
#    # Storage pool default deleted
#    
#    # % lxc storage list
#    # +---------------+--------+--------------+-------------+---------+---------+
#    # |     NAME      | DRIVER |    SOURCE    | DESCRIPTION | USED BY |  STATE  |
#    # +---------------+--------+--------------+-------------+---------+---------+
#    # | mylxpool-60gb | zfs    | myzpool-60gb |             | 1       | CREATED |
#    # +---------------+--------+--------------+-------------+---------+---------+
#    
