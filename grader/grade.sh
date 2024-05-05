if [ "$1" == "" ]; then
    echo "Usage: ./grade.sh /path/to/your/assignmentN"
    exit 1
fi
# find the scipt dir
location=$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)
student_code=$(dirname $1)
assignment=$(basename $1)
# if have podman use it instead of docker, it is better
which podman && cmd=podman || cmd=docker
# build and run docker with custom command
$cmd build --quiet -t selenium -f Dockerfile $location && \
$cmd run -it --rm \
         --mount type=bind,source=$location/..,target=/class_code,readonly \
         --mount type=bind,source=$student_code,target=/student_code,readonly \
         selenium sh -c "python /class_code/grader/grade.py --override=/student_code/$assignment"
