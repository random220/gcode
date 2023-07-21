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

color_bg() {
    local color=$1
    echo '\x1b[48;5;'$color'm'
}
color_fg() {
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
            m=$(expr $y % 8)
            if [[ $m == 0 ]]; then
                echo; echo
            fi
            echo -n -e $(color_bg $x)$(color_fg 0)' '$x' '$(color_fg $x)$(color_bg $y)'  '$(color_fg 0)$y' '$(color_reset)$(color_fg $y)''$(color_reset)'    '
            y=$(( y+1 ))
        done
        x=$(( x+1 ))
    done
else
    x=$c1
    y=$c2
    z=0
    while [[ $z -lt 255 ]]; do
        m=$(expr $z % 8)
        if [[ $m == 0 ]]; then
            echo; echo
        fi
        echo -n -e $(color_bg $x)$(color_fg 0)' '$x' '$(color_fg $x)$(color_bg $y)'  '$(color_fg 0)$y' '$(color_reset)$(color_fg $y)$(color_bg $z)''$(color_reset)$(color_bg $z)$(color_fg 0)' '$z'   '$(color_reset)$(color_fg $z)''$(color_reset)'    '
        z=$(( z+1 ))
    done
fi




