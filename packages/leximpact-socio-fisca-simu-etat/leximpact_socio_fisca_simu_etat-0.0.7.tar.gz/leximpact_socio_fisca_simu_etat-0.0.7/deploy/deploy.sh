#!/bin/bash
echo "Starting deploy"
eval $(ssh-agent -s)
ssh-add <(echo "$SSH_PRIVATE_KEY")
'[[ -f /.dockerenv ]] && mkdir -p ~/.ssh && echo -e "Host *\n\tStrictHostKeyChecking no\n\tLogLevel quiet\n" > ~/.ssh/config'
ssh leximpact@$INTEGRATION_IP "cd $CI_PROJECT_NAME && git fetch --all && git reset --hard origin/master && git checkout $CI_COMMIT_REF_NAME && git pull && exit"
ssh leximpact@$INTEGRATION_IP "cd $CI_PROJECT_NAME && poetry install && exit"
ssh leximpact@$INTEGRATION_IP "systemctl --user restart leximpactserver.service"