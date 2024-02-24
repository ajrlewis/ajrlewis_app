#!/usr/bin/env bash

# Gandi utilities script for hosting project

init() {
  if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "Git repository already exists."
  else
    git init
    echo "Git repository initialized."
  fi
}

add_remotes(){
  git remote add gandi git+ssh://${GANDI_USER}@${GANDI_SERVER}/${GANDI_REPO}
  git remote add github git@github.com:${GITHUB_USER}/${APP_NAME}_app.git
  echo "Git repository remotes added."
}

push() {
  git push --force gandi master
  git push --force github master
  echo "Push to git remotes."
}

deploy() {
  ssh ${GANDI_USER}@${GANDI_SERVER} deploy default.git
  ssh ${GANDI_USER}@${GANDI_SERVER} clean default.git
  echo "Deployed to Gandi."
  echo "Cleaned untracked files in repository."
}

backup_db() {
  date=$(date '+%Y-%m-%d %H:%M:%S')
  echo ssh ${GANDI_USER}@${GANDI_SERVER} "mysqldump -u root -p --database ${APP_NAME}_db" > backups/${APP_NAME}_db ${date}.sql
  echo "Backup remote database."
}

# reset_log() {
#   # https://${GANDI_USER}.admin.sd6.gpaas.net/log/www/uwsgi.log
#   # echo "" > /srv/data/var/log/www/uwsgi.log
# }

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  source .env
  if [[ "$1" == "init" ]]; then
    init
    add_remotes
  elif [[ "$1" == "push" ]]; then
    push
  elif [[ "$1" == "deploy" ]]; then
    deploy
  else
    echo "No command given!"
  fi
fi
