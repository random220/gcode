#!/bin/bash

REPO='git-aws:repos/priv-intel-VTd_SIOV_TR--multirel.git'

function main() {
  if [[ ! -d data ]]; then
    mkdir data
  fi
  if [[ ! -d data/.git ]]; then
    (
      cd data
      git init
      git remote add origin $REPO
      git fetch --all
    )
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

  while true; do
    (
      cd data
      stashit
      refetch
      stashit
    )
    sleep 300
  done
}


function refetch() {
  local NOW=$(date +%s)
  local DATE=$(date)
  local REMOTE=$(git remote -v | grep fetch|awk '{print $2}')

  if [[ $REMOTE == '' ]]; then
    REMOTE=$REPO
    git remote add origin $REMOTE
  else
    git remote rm origin
    git remote add origin $REMOTE
  fi
  git fetch --all
}

function stashit() {
  local NOW=$(date +%s)
  local DATE=$(date)
  local REMOTE==$(git remote -v | grep fetch|awk '{print $2}')

  local r=$(git rev-list --all -1)
  echo $r >.git/HEAD
  rsync -a --delete .git/refs/ ../metadata/refs/
  (
    cd ../metadata
    rm -rf refs/heads
    git add -Af
    git commit -m "$NOW $DATE REMOTE: $REMOTE"
  )
  
  local TIPS=$(git rev-list --branches --remotes --children --tags|grep -v ' ')
  local BRANCHES=$(git branch|grep -v '\*')
  local TAGS=$(git tag)
  
  # Create branches to anchor all tip revisions found above
  local n=0
  local rev
  for rev in $TIPS; do
    let n+=1
    git branch __b__${NOW}__${n} $rev
  done
  
  # Delete all local branches and tags that existed before we created our
  # anchor branches
  if [[ $BRANCHES != '' ]]; then
    git branch -D $BRANCHES
  fi
  if [[ $TAGS != '' ]]; then
    git tag -d $TAGS
  fi
}


main

