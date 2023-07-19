#!/bin/bash

# https://en.wikipedia.org/wiki/ANSI_escape_code

# echo -e '\x1b[48;5;COLORm  #background
# echo -e '\x1b[38;5;COLORm  #foreground
# echo -e '\x1b[0m           #reset

x=0
while [[ $x -le 255 ]]; do
    echo -n $x'   :  '
    echo -n -e '\x1b[48;5;'$x'm        \x1b[0m  --  '
    echo -e '\x1b[48;5;15m\x1b[38;5;'$x'mXXXXXXXX\x1b[0m'
    x=$(( x+1 ))
done
echo
echo -e '\x1b[48;5;111m\x1b[38;5;236mXXXXXXXX\x1b[0m'
