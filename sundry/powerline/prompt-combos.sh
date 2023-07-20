#!/bin/bash

# https://en.wikipedia.org/wiki/ANSI_escape_code

# echo -e '\x1b[48;5;COLORm  #background
# echo -e '\x1b[38;5;COLORm  #foreground
# echo -e '\x1b[0m           #reset

c1="$1"
c2="$2"
c3="$3"

if [[ $c1 == '' ]]; then
    c1a=0
    c1z=255
else
    c1a=$c1
    c1z=$c1
fi
if [[ $c2 == '' ]]; then
    c2a=0
    c2z=255
else
    c2a=$c2
    c2z=$c2
fi
if [[ $c3 == '' ]]; then
    c3a=0
    c3z=255
else
    c3a=$c3
    c3z=$c3
fi

color_back() {
    local color=$1
    echo '\x1b[48;5;'$color'm'
}
color_fore() {
    local color=$1
    echo '\x1b[38;5;'$color'm'
}
color_reset() {
    echo '\x1b[0m'
}

if [[ $c2 == '' ]]; then
    x=$c1a
    while [[ $x -le $c1z ]]; do
        y=$c2a
        while [[ $y -le $c2z ]]; do
            echo -e $(color_back $x)' '$x' '$(color_fore $x)$(color_back $y)'  '$y' '$(color_reset)$(color_fore $y)''$(color_reset)
            echo
            y=$(( y+1 ))
        done
        x=$(( x+1 ))
    done
else
    x=$c1
    y=$c2
    z=0
    while [[ $z -lt 255 ]]; do
        echo -e $(color_back $x)' '$x' '$(color_fore $x)$(color_back $y)'  '$y' '$(color_reset)$(color_fore $y)$(color_back $z)''$(color_reset)$(color_back $z)' '$z'   '$(color_reset)$(color_fore $z)''$(color_reset)
        echo
        z=$(( z+1 ))
    done
fi




