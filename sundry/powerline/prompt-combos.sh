#!/bin/bash

# https://en.wikipedia.org/wiki/ANSI_escape_code

# echo -e '\x1b[48;5;COLORm  #background
# echo -e '\x1b[38;5;COLORm  #foreground
# echo -e '\x1b[0m           #reset

c1="$1"
c2="$2"
c3="$3"
x=0
y=255
splitarg() {
    arg=$1
    x=$(sed 's/-.*//' <<<"$arg")
    y=$(sed 's/^.*-//' <<<"$arg")
    if [[ $x == '' ]]; then
        x=0
    fi
    if [[ $y == '' ]]; then
        y=255
    fi
}

splitarg $1; c1a=$x; c1z=$y
splitarg $2; c2a=$x; c2z=$y
splitarg $3; c3a=$x; c3z=$y

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




