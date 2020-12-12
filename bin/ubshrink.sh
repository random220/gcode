#!/bin/bash

#killall -9 apt-get
#killall -9 dpkg
dpkg --configure -a
apt-get -y update
apt-get -y dist-upgrade

#uname -a
#Linux ub20 5.4.0-58-generic #64-Ubuntu SMP Wed Dec 9 08:16:25 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux

#uname -a|awk '{print $3}'
# 5.4.0-58-generic

#uname -a|awk '{print $3}'|perl -pe 's/^([\d\.\-]+\d).*$/$1/'
#5.4.0-58

#uname -a|awk '{print $3}'|perl -pe 's/^([\d\.\-]+\d).*$/$1/; s/-/./g'
#5.4.0.58

v=$(uname -a|awk '{print $3}'|perl -pe 's/^([\d\.\-]+\d).*$/$1/; s/-/./g')

#dpkg -l |egrep "$v"
#ii  linux-generic                        5.4.0.58.61                       amd64        Complete Generic Linux kernel and headers
#ii  linux-headers-5.4.0-58               5.4.0-58.64                       all          Header files related to Linux kernel version 5.4.0
#ii  linux-headers-5.4.0-58-generic       5.4.0-58.64                       amd64        Linux kernel headers for version 5.4.0 on 64 bit x86 SMP
#ii  linux-headers-generic                5.4.0.58.61                       amd64        Generic Linux kernel headers
#ii  linux-image-5.4.0-58-generic         5.4.0-58.64                       amd64        Signed kernel image generic
#ii  linux-image-generic                  5.4.0.58.61                       amd64        Generic Linux kernel image
#ii  linux-modules-5.4.0-58-generic       5.4.0-58.64                       amd64        Linux kernel extra modules for version 5.4.0 on 64 bit x86 SMP
#ii  linux-modules-extra-5.4.0-58-generic 5.4.0-58.64                       amd64        Linux kernel extra modules for version 5.4.0 on 64 bit x86 SMP


#dpkg -l |egrep "$v" | awk '{print $2}'
#linux-generic
#linux-headers-5.4.0-58
#linux-headers-5.4.0-58-generic
#linux-headers-generic
#linux-image-5.4.0-58-generic
#linux-image-generic
#linux-modules-5.4.0-58-generic
#linux-modules-extra-5.4.0-58-generic

#dpkg -l |egrep "$v" | awk '{print $2}'|sed 's/-[0-9].*//' | sort -u
#linux-generic
#linux-headers
#linux-headers-generic
#linux-image
#linux-image-generic
#linux-modules
#linux-modules-extra

#dpkg -l |egrep "$v" | awk '{print $2}'|sed 's/-[0-9].*//' | sort -u|xargs|sed 's/ /|/g'
#linux-generic|linux-headers|linux-headers-generic|linux-image|linux-image-generic|linux-modules|linux-modules-extra


p=$(dpkg -l |egrep "$v" | awk '{print $2}'|sed 's/-[0-9].*//' | sort -u|xargs|sed 's/ /|/g')

#dpkg -l|egrep "$p"|egrep -v "$v"
#ii  linux-headers-5.4.0-52               5.4.0-52.57                       all          Header files related to Linux kernel version 5.4.0
#ii  linux-headers-5.4.0-52-generic       5.4.0-52.57                       amd64        Linux kernel headers for version 5.4.0 on 64 bit x86 SMP
#ii  linux-image-5.4.0-52-generic         5.4.0-52.57                       amd64        Signed kernel image generic
#ii  linux-modules-5.4.0-52-generic       5.4.0-52.57                       amd64        Linux kernel extra modules for version 5.4.0 on 64 bit x86 SMP
#ii  linux-modules-extra-5.4.0-52-generic 5.4.0-52.57                       amd64        Linux kernel extra modules for version 5.4.0 on 64 bit x86 SMP

#dpkg -l|egrep "$p"|egrep -v "$v"|awk '{print $2}'
#linux-headers-5.4.0-52
#linux-headers-5.4.0-52-generic
#linux-image-5.4.0-52-generic
#linux-modules-5.4.0-52-generic
#linux-modules-extra-5.4.0-52-generic

dpkg -l|egrep "$p"|egrep -v "$v"|awk '{print $2}'|xargs -L 1 apt-get -y remove
dpkg -l|egrep "$p"|egrep -v "$v"|awk '{print $2}'|xargs -L 1 apt-get -y purge
apt autoremove


