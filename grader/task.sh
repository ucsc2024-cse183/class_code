set -e
docker stop $(docker ps -a  | grep selenium | awk '{print $1}')	|| true
docker container prune --force || true
echo '{"status": "failure"}' > task.output.json
git clone https://mdipierro:$(cat ~/token)@github.com/ucsc2024-cse183/$1-code.git > /dev/null
path=`pwd`/$1-code/$2
cd class_code/grader
./grade.sh $path && echo '{"status": "success"}' > ../../task.output.json
