umask 077

if [[ $SHLVL == 1 ]]; then
    cd
fi
export PATH="$HOME/gcode/bin:$PATH"
if [[ -f ~/.aliases ]]; then
    . ~/.aliases
fi
