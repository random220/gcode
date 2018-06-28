if [[ -e $HOME/.aliases ]]; then
  . $HOME/.aliases
fi

if [[ -f $HOME/.bashrc-perforce ]]; then
  . $HOME/.bashrc-perforce
fi

if [[ -e $HOME/.localsetup ]]; then
  . $HOME/.localsetup
fi

