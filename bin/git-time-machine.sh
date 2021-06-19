#!/bin/bash

REPO='/Users/omandal/sb/repos/backup-2021-02-20.git'
REPO='git-aws:repos/priv-intel-VTd_SIOV_TR--multirel.git'
REPO='omandal@sc-dbc2131:/dbc/sc-dbc2131/omandal/repos/backup-2020-09-27.git'

function init_main() {
  ensure_data_dirs
  for REPO in \
        omandal@sc-dbc2131:/dbc/sc-dbc2131/omandal/repos/backup-2020-09-27.git \
        omandal@sc-dbc2131:/dbc/sc-dbc2131/omandal/repos/backup-2020-09-30.git \
        omandal@sc-dbc2131:/dbc/sc-dbc2131/omandal/repos/backup-2020-10-01.git \
        omandal@sc-dbc2131:/dbc/sc-dbc2131/omandal/repos/backup-2020-10-03.git \
        omandal@sc-dbc2131:/dbc/sc-dbc2131/omandal/repos/backup-2020-10-10.git \
        omandal@sc-dbc2131:/dbc/sc-dbc2131/omandal/repos/backup-2020-10-12.git \
        omandal@sc-dbc2131:/dbc/sc-dbc2131/omandal/repos/backup-2020-10-13.git \
        omandal@sc-dbc2131:/dbc/sc-dbc2131/omandal/repos/backup-2020-10-28.git \
        omandal@sc-dbc2131:/dbc/sc-dbc2131/omandal/repos/backup-2020-11-03.git \
        omandal@sc-dbc2131:/dbc/sc-dbc2131/omandal/repos/backup-2020-11-05.git \
        omandal@sc-dbc2131:/dbc/sc-dbc2131/omandal/repos/backup-2020-11-11.git \
        omandal@sc-dbc2131:/dbc/sc-dbc2131/omandal/repos/backup-2020-12-10.git \
        omandal@sc-dbc2131:/dbc/sc-dbc2131/omandal/repos/backup-2020-12-17.git \
        omandal@sc-dbc2131:/dbc/sc-dbc2131/omandal/repos/backup-2020-12-19.git \
        omandal@sc-dbc2131:/dbc/sc-dbc2131/omandal/repos/backup-2021-01-11.git \
        omandal@sc-dbc2131:/dbc/sc-dbc2131/omandal/repos/backup-2021-01-14.git \
        omandal@sc-dbc2131:/dbc/sc-dbc2131/omandal/repos/backup-2021-01-24.git \
        omandal@sc-dbc2131:/dbc/sc-dbc2131/omandal/repos/backup-2021-01-28.git \
        omandal@sc-dbc2131:/dbc/sc-dbc2131/omandal/repos/backup-2021-02-02.git \
        omandal@engops-db2:/b/cb-repos/backup-2021-02-03.git \
        omandal@sc-dbc2131:/dbc/sc-dbc2131/omandal/repos/backup-2021-02-03.git \
        omandal@engops-db2:/b/cb-repos/backup-2021-02-04.git \
        omandal@engops-db2:/b/cb-repos/backup-2021-02-05.git \
        omandal@engops-db2:/b/cb-repos/backup-2021-02-10.git \
        omandal@engops-db2:/b/cb-repos/backup-2021-02-15.git \
        omandal@engops-db2:/b/cb-repos/backup-2021-02-16.git \
        omandal@engops-db2:/b/cb-repos/backup-2021-02-18.git \
        /Users/omandal/sb/repos/backup-2021-02-20.git \
        omandal@engops-db2:/b/cb-repos/backup-2021-02-20.git \
        /Users/omandal/sb/repos/backup-2021-02-25.git \
        omandal@engops-db2:/b/cb-repos/backup-2021-02-25.git \
        /Users/omandal/sb/repos/backup-2021-03-12.git \
        omandal@engops-db2:/b/cb-repos/backup-2021-03-12.git \
        /Users/omandal/sb/repos/backup-2021-03-13.git \
        omandal@engops-db2:/b/cb-repos/backup-2021-03-13.git \
        /Users/omandal/sb/repos/backup-2021-03-31.git \
        omandal@engops-db2:/b/cb-repos/backup-2021-03-31.git \
        /Users/omandal/sb/repos/backup-2021-04-04.git \
        omandal@engops-db2:/b/cb-repos/backup-2021-04-08.git \
        omandal@sc-dbc2131:/dbc/sc-dbc2131/omandal/repos/backup-2021-04-08.git \
        /Users/omandal/sb/repos/backup-2021-04-13.git \
        omandal@engops-db2:/b/cb-repos/backup-2021-04-13.git \
        /Users/omandal/sb/repos/backup-2021-04-18.git \
        omandal@engops-db2:/b/cb-repos/backup-2021-04-18.git \
        /Users/omandal/sb/repos/backup-2021-05-14.git \
        omandal@engops-db2:/b/cb-repos/backup-2021-05-14.git \
        /Users/omandal/sb/repos/backup-2021-05-19.git \
        omandal@engops-db2:/b/cb-repos/backup-2021-05-19.git \
        /Users/omandal/sb/repos/backup-2021-06-02.git \
        omandal@engops-db2:/b/cb-repos/backup-2021-06-02.git \
        /Users/omandal/sb/repos/backup-2021-06-07.git \
        omandal@engops-db2:/b/cb-repos/backup-2021-06-07.git \
        /Users/omandal/sb/repos/backup-2021-06-17.git \
        omandal@engops-db2:/b/cb-repos/backup-2021-06-17.git \
        ; do
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
  local R=$RANDOM

  local TIPS=$(git rev-list --branches --remotes --children --tags|grep -v ' ')
  local BRANCHES=$(git branch|grep -v '\*')
  local TAGS=$(git tag)
  
  # Create branches to anchor all tip revisions found above
  local n=0
  local rev
  for rev in $TIPS; do
    let n+=1
    git branch __b__${NOW}__${R}__${n} $rev
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

init_main

