#!/bin/bash

function main() {
  :
}

function test_main() {
  local REPOS=(
    backup-2021-02-20.git
    backup-2021-02-25.git
    backup-2021-03-12.git
    backup-2021-03-13.git
    backup-2021-03-31.git
    backup-2021-04-04.git
    backup-2021-04-13.git
    backup-2021-04-18.git
    backup-2021-05-14.git
    backup-2021-05-19.git
    backup-2021-06-02.git
    backup-2021-06-07.git
    backup-2021-06-17.git
  )
  if [[ ! -d data ]]; then
    mkdir data
  fi
  if [[ ! -d data/.git ]]; then
    (cd data && git init)
  fi
  if [[ ! -d metadata ]]; then
    mkdir metadata
  fi
  if [[ ! -d metadata/.git ]]; then
    (
      cd metadata
      git init
      git config user.email root@localhost
      git config user.name root
    )
  fi

  local repo
  for repo in ${REPOS[@]}; do
    ( cd data && stashit $repo )
  done
}

function stashit() {
  local repo=$1
  git remote add a file:///Users/omandal/sb/repos/$repo
  git fetch --all
  local r=$(git rev-list --all -1)
  echo $r >.git/HEAD
  rsync -a --delete .git/refs/ ../metadata/refs/
  (
  cd ../metadata
  rm -rf refs/heads
  git add -Af
  git commit -m "$(date +%s) $(date) $repo"
  )
  
  local TIPS=$(git rev-list --branches --remotes --children --tags|grep -v ' ')
  local BRANCHES=$(git branch|grep -v '\*')
  local TAGS=$(git tag)
  
  local NOW=$(date +%s)
  local n=0
  local rev
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


test_main
