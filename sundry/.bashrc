if [[ -e $HOME/.gcode/.aliases ]]; then
  . $HOME/.gcode/.aliases
fi

if [[ -f $HOME/.gcode/.bashrc-perforce ]]; then
  . $HOME/.gcode/.bashrc-perforce
fi

if [[ -e $HOME/.local/.bashrc ]]; then
  . $HOME/.local/.bashrc
fi

# export LC_ALL=C.UTF-8
# export LANG=C.UTF-8
# export LC_ALL=en.UTF-8
# export LANG=en.UTF-8
LANG=''
export LANG
if [[ $LANG == '' ]]; then
    LANG=$(locale -a | grep 'en_US.UTF-8')
fi
if [[ $LANG == '' ]]; then
    LANG=$(locale -a | grep 'C.UTF-8')
fi
if [[ $LANG == '' ]]; then
    LANG=POSIX
fi
export LC_ALL=$LANG

function rst() {
    # https://apple.stackexchange.com/questions/446859/when-pasting-in-terminal-app-00-is-pasted-at-the-start-and-01-at-the-end
    printf '\e[?2004l'
}
