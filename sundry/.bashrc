if [[ -e $HOME/.aliases ]]; then
  . $HOME/.aliases
fi

if [[ -f $HOME/.bashrc-perforce ]]; then
  . $HOME/.bashrc-perforce
fi

if [[ -e $HOME/.localsetup ]]; then
  . $HOME/.localsetup
fi

alias d='git show 10c0306:$f >l.c; git show 4a221be:$f >r.c; git show d48cef2:$f >w.c; vimdiff l.c r.c'
alias d2='vimdiff w.c $f'
