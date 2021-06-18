function common() {
  git fetch --all
  r=$(git rev-list --all -1)
  echo $r >.git/HEAD
  rsync -a --delete .git/refs/ ../y/refs/
  (
  cd ../y
  git add -Af
  git commit -m "$(date +%s) $(date)"
  )
  
  TIPS=$(git rev-list --branches --remotes --children --tags|grep -v ' ')
  BRANCHES=$(git branch|grep -v '\*')
  TAGS=$(git tag)
  
  NOW=$(date +%s)
  n=0
  for rev in $TIPS; do
    let n+=1
    git branch b_${NOW}_${n} $rev
  done
  
  if [[ $BRANCHES != '' ]]; then
    git branch -D $BRANCHES
  fi
  if [[ $TAGS != '' ]]; then
    git tag -d $TAGS
  fi
  
  git remote rm a
}

#----------------

#git init
#git remote add a ../backup-2021-02-20.git
#common

#git remote add a ../backup-2021-02-25.git
#common

#git remote add a ../backup-2021-03-12.git
#common

#git remote add a ../backup-2021-03-13.git
#common

git remote add a ../backup-2021-03-31.git
common


