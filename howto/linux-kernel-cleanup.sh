myversion=$(uname -a|awk '{print $3}')
echo "My kernel version: $myversion"
cmd="rpm -qa|grep kernel|grep -v "$myversion"|sed 's/^[^0-9]*//'|sort -u|xargs|sed 's/ /|/g'"
echo "cmd: $cmd"
oldversions=$(bash -c "$cmd")
if [[ $oldversions == '' ]]; then
  exit 0
fi
echo "oldversions: $oldversions"
packages_to_remove=$(rpm -qa|egrep "\-$oldversions")
printf "$packages_to_remove"
echo
read -p "Remove these packages? [YES/no]" yn
if [[ $yn == 'YES' ]]; then
  remove_cmd="yum -y remove "$(echo "$packages_to_remove"|xargs)
  echo
  printf "$remove_cmd"
  echo
  read -p "This command OK? [YES/no]" yn
  if [[ $yn == "YES" ]]; then
    bash -c "$remove_cmd"
  fi
fi
