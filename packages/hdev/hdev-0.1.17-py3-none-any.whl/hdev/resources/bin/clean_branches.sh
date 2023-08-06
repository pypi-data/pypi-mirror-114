#!/bin/bash

# Clean up old branches
git fetch --prune

# See https://www.erikschierboom.com/2020/02/17/cleaning-up-local-git-branches-deleted-on-a-remote/
OLD_BRANCHES=$(
  git for-each-ref --format '%(refname:short) %(upstream:track)' refs/heads \
  | awk '$2 == "[gone]" {print $1}'
)

if [ "${OLD_BRANCHES}" ]
then
  LOG_FILE=".git/hdev_removed_branches.log"
  echo "Removing old branches (see: $LOG_FILE)"
  echo "$OLD_BRANCHES" | xargs git branch -D | tee -a $LOG_FILE
  echo "Record of branches removed written to: $LOG_FILE"
fi
