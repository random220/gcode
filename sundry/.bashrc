if [[ -e $HOME/.aliases ]]; then
  . $HOME/.aliases
fi

if [[ -f $HOME/.bashrc-perforce ]]; then
  . $HOME/.bashrc-perforce
fi

if [[ -e $HOME/.local/.bashrc ]]; then
  . $HOME/.local/.bashrc
fi

# export LC_ALL=C.UTF-8
# export LANG=C.UTF-8
# export LC_ALL=en.UTF-8
# export LANG=en.UTF-8
export LANG=en_US.UTF-8
export LC_ALL=$LANG

##-----------------------------------------------------
## synth-shell-greeter.sh
#if [ -f $HOME/.config/synth-shell/synth-shell-greeter.sh ] && [ -n "$( echo $- | grep i )" ]; then
#	source $HOME/.config/synth-shell/synth-shell-greeter.sh
#fi

##-----------------------------------------------------
## synth-shell-prompt.sh
if [ -f $HOME/.config/synth-shell/synth-shell-prompt.sh ] && [ -n "$( echo $- | grep i )" ]; then
	source $HOME/.config/synth-shell/synth-shell-prompt.sh
fi

##-----------------------------------------------------
## better-ls
if [ -f $HOME/.config/synth-shell/better-ls.sh ] && [ -n "$( echo $- | grep i )" ]; then
	source $HOME/.config/synth-shell/better-ls.sh
fi

##-----------------------------------------------------
## alias
if [ -f $HOME/.config/synth-shell/alias.sh ] && [ -n "$( echo $- | grep i )" ]; then
	source $HOME/.config/synth-shell/alias.sh
fi

##-----------------------------------------------------
## better-history
if [ -f $HOME/.config/synth-shell/better-history.sh ] && [ -n "$( echo $- | grep i )" ]; then
	source $HOME/.config/synth-shell/better-history.sh
fi

