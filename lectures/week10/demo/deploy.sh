rsync -avz --exclude web/compose-py4web/apps/ci/databases --exclude web/compose-py4web/apps/group_preferences/databases --exclude web/compose-py4web/apps/.service --exclude web/compose-py4web/apps/_dashboard web mdipierro@unofficialtools.com:~/
ssh mdipierro@unofficialtools.com  "cd web && docker-compose restart"
