if [[ -e $HOME/.aliases ]]; then
  . $HOME/.aliases
fi

if [[ -f ~/.bashrc-perforce ]]; then
  . $HOME/.bashrc-perforce
fi

if [[ -e ~/.localsetup ]]; then
  . $HOME/.localsetup
fi

