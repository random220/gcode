#!/bin/bash

export PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin

id=$(id -u)
if [[ $id != 0 ]]; then
  echo not root
  exit 0
fi

if [[ ! -f /etc/hosts.open ]]; then
  cat /etc/hosts >/etc/hosts.open
fi
if [[ ! -f /etc/hosts.close ]]; then
  cat /etc/hosts >/etc/hosts.close
  echo '127.0.0.1 facebook.com' >>/etc/hosts.close
  echo '127.0.0.1 www.facebook.com' >>/etc/hosts.close
  echo '127.0.0.1 tiktok.com' >>/etc/hosts.close
  echo '127.0.0.1 www.tiktok.com' >>/etc/hosts.close
  echo '127.0.0.1 instagram.com' >>/etc/hosts.close
  echo '127.0.0.1 www.instagram.com' >>/etc/hosts.close
  echo '127.0.0.1 discord.com' >>/etc/hosts.close
  echo '127.0.0.1 www.discord.com' >>/etc/hosts.close
  echo '127.0.0.1 netflix.com' >>/etc/hosts.close
  echo '127.0.0.1 www.netflix.com' >>/etc/hosts.close
fi

if [[ $1 == 'open' ]]; then
  cat /etc/hosts.open >/etc/hosts
  date=$(date)
  echo "$date opened" >>/etc/hosts.activity
  exit 0
fi

if [[ $1 == 'close' ]]; then
  cat /etc/hosts.close >/etc/hosts
  date=$(date)
  echo "$date closed" >>/etc/hosts.activity
  exit 0
fi

if [[ $1 == 'check' ]]; then
  cmp -s /etc/hosts.close /etc/hosts
  if [[ $? != 0 ]]; then
    f=$(find /etc/hosts -type f -mmin +10)
    if [[ $f == '/etc/hosts' ]]; then
      cat /etc/hosts.close >/etc/hosts
      date=$(date)
      echo "$date closed" >>/etc/hosts.activity
      exit 0
    fi
  fi
fi

exit 0

