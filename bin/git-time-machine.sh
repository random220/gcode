#!/bin/bash

umask 022

REPO='git-aws:repos/priv-intel-VTd_SIOV_TR--multirel.git'

function main() {
  ensure_data_dirs
  (
    cd data
    refetch
    save_refs
  )
}

function refetch() {
  anchor_branch_tips
  git remote rm origin
  git remote add origin $REPO
  git fetch --all
}

function save_refs() {
  local NOW=$(date +%s)
  local DATE=$(date)
  local REMOTE=$(git remote -v | grep fetch|awk '{print $2}')

  rm -rf ../metadata/branches ../metadata/tags
  mkdir ../metadata/branches ../metadata/tags

  >../metadata/packed-revs

  local branches=$(git branch -r|sed 's/^..//')
  local branch
  for branch in $branches; do
    rev=$(git rev-list -1 $branch)
    justbranch=$(echo "$branch" | sed 's/^origin\///')
    dest_path="../metadata/branches/$justbranch"
    mkdir -p $(dirname "$dest_path")
    echo $rev >"$dest_path"
    echo "$rev branches/$justbranch" >>../metadata/packed-revs
  done

  local tags=$(git tag)
  local tag
  for tag in $tags; do
    rev=$(git rev-list -1 $tag)
    dest_path="../metadata/tags/$tag"
    mkdir -p $(dirname "$dest_path")
    echo $rev >"$dest_path"
    echo "$rev tags/$tag" >>../metadata/packed-revs
  done
  (
    cd ../metadata
    git add -Af
    git commit -m "${NOW} ${DATE} REMOTE: ${REMOTE}"
  )
}

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
      refetch
      save_refs
    )
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
      git remote add origin whatever
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

function anchor_branch_tips() {
  local NOW=$(date +%s)
  local R=$RANDOM

  local TIPS=$(git rev-list --all --children|grep -v ' ')
  local BRANCHES=$(git branch|grep -v '>'|sed 's/^..//')
  local TAGS=$(git tag)
  
  # Create branches to anchor all tip revisions found above
  local n=0
  local _hash
  for _hash in $TIPS; do
    let n+=1
    git branch __b__${NOW}__${R}__${n} $_hash
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

#init_main
main

