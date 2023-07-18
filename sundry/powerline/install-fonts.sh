#!/bin/bash
rm -rf ~/__powerline
mkdir ~/__powerline
cd ~/__powerline
git clone https://github.com/powerline/fonts.git --depth=1
cd fonts
./install.sh
cd
rm -rf ~/__powerline
