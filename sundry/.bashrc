if [[ -e $HOME/.aliases ]]; then
  . $HOME/.aliases
fi

if [[ -f $HOME/.bashrc-perforce ]]; then
  . $HOME/.bashrc-perforce
fi

if [[ -e $HOME/.local/.bashrc ]]; then
  . $HOME/.local/.bashrc
fi

#export LC_ALL=C.UTF-8
#export LANG=C.UTF-8

