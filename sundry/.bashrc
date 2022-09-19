if [[ -e $HOME/.aliases ]]; then
  . $HOME/.aliases
fi

if [[ -f $HOME/.bashrc-perforce ]]; then
  . $HOME/.bashrc-perforce
fi

if [[ -e $HOME/.localsetup ]]; then
  . $HOME/.localsetup
fi

if [[ -e $HOME/.puresetup ]]; then
  . $HOME/.puresetup
fi

#export LC_ALL=C.UTF-8
#export LANG=C.UTF-8

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
if command -v pyenv 1>/dev/null 2>&1; then
  eval "$(pyenv init -)" 
fi
