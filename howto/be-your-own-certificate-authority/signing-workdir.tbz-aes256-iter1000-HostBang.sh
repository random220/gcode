#!/bin/bash

if [[ ! -f '/usr/bin/lsb_release' ]]; then
  echo 'You need to be on a Ubuntu machine'
  exit 1
fi

rel=$(/usr/bin/lsb_release -d)
if [[ $rel =~ Ubuntu ]]; then
  # Description:    Ubuntu 18.04.2 LTS

  # That's good
  :
else
  echo 'You need to be on a Ubuntu machine'
  exit 1
fi

if [[ -d 'workdir' ]]; then
  echo 'WARNING: Directory "workdir" already exists here.'
  echo
  echo -n 'OK to delete? [y/n]: '
  read response
  if [[ $response == 'y' ]]; then
    echo -n 'Are you sure? [y/n]: '
    read response
    if [[ $response == 'y' ]]; then
      rm -rf 'workdir'
    fi
  fi
fi

if [[ -d 'workdir' ]]; then
  echo 'Please manually delete workdir'
  exit 1
fi

echo 'Hint: Host!'
echo
openssl enc -d -aes256 -iter 1000 <signing-workdir.tbz-aes256-iter1000-HostBang | tar xfj -


if [[ ! -d 'workdir' ]]; then
  echo 'Extraction failed'
  exit 1
fi

cd 'workdir'
git reset --hard


