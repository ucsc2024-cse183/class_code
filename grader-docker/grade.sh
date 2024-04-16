if [ "$1" == "" ]; then
    echo "Usage: ./grade.sh /path/to/your/assignmentN"
    exit 1
fi
# find the scipt dir
location=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
# if have podman use it instead of docker, it is better
which podman && cmd=podman || cmd=docker
# build and run docker with custom command
$cmd build $location -t selenium -f Dockerfile && $cmd run -it --mount type=bind,source=$(dirname $1),target=/repo selenium sh -c "git init class_code -b main && cd class_code && git remote add origin https://github.com/ucsc2024-cse183/class_code.git && git config core.sparsecheckout true && (echo 'grader/' >> .git/info/sparse-checkout) && git pull --depth=1 origin main && cd .. && venv/bin/python class_code/grader/grade.py --override=/repo/$(basename $1)"
