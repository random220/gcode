#!/bin/bash

REPO='/Users/omandal/sb/repos/backup-2021-02-20.git'
REPO='git-aws:repos/priv-intel-VTd_SIOV_TR--multirel.git'

function init_main() {
  ensure_data_dirs
  for REPO in \
        /Users/omandal/sb/repos/backup-2021-02-25.git \
        /Users/omandal/sb/repos/backup-2021-03-12.git \
        /Users/omandal/sb/repos/backup-2021-03-13.git \
        /Users/omandal/sb/repos/backup-2021-03-31.git \
        /Users/omandal/sb/repos/backup-2021-04-04.git \
        /Users/omandal/sb/repos/backup-2021-04-13.git \
        /Users/omandal/sb/repos/backup-2021-04-18.git \
        /Users/omandal/sb/repos/backup-2021-05-14.git \
        /Users/omandal/sb/repos/backup-2021-05-19.git \
        /Users/omandal/sb/repos/backup-2021-06-02.git \
        /Users/omandal/sb/repos/backup-2021-06-07.git \
        /Users/omandal/sb/repos/backup-2021-06-17.git; do
    (
      cd data
      save_refs
      refetch
      save_refs
    )
  done
}

function main() {
  ensure_data_dirs
  while true; do
    (
      cd data
      save_refs
      refetch
      save_refs
    )
    sleep 300
  done
}

function ensure_data_dirs() {
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
}

function refetch() {
  local NOW=$(date +%s)
  local DATE=$(date)

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

  # Now refetch
  git remote rm origin
  git remote add origin $REPO
  git fetch --all
}

function save_refs() {
  local NOW=$(date +%s)
  local DATE=$(date)
  local REMOTE=$(git remote -v | grep fetch|awk '{print $2}')

  rsync -a --delete .git/refs/ ../metadata/refs/
  (
    cd ../metadata
    rm -rf refs/heads
    git add -Af
    git commit -m "$NOW $DATE REMOTE: $REMOTE"
  )
}

main

