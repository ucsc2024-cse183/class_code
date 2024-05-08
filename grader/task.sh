set -e
echo "run ${CI_RUN_ID}"
echo "cleaning up memory..."
docker stop $(docker ps -a  | grep selenium | awk '{print $1}')	|| true
docker container prune --force || true
echo '{"status": "failure"}' > task.output.json
echo "cloning student repo..."
git clone https://${github_credentials}@github.com/ucsc2024-cse183/$1-code.git > /dev/null
path=`pwd`/$1-code/$2
echo "print repos info..."
find ./ -name ".git" -type d | sed "s,.git$,," | xargs -i sh -c 'cd {}; echo "{}:$(git config --get remote.origin.url)/commit/$(git rev-parse HEAD)"' | sed 's/\/\/.*@/\/\//' | sed 's/\.git//'
echo "grading..."
cd class_code/grader
./grade.sh $path && echo '{"status": "success"}' > ../../task.output.json
