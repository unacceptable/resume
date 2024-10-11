#!/usr/bin/env bash
set -e

function random_string() {
    cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n 1
}

export RANDOM_STRING=random_string

docker build -t resume:local . &&

docker run -it --name "resume-${RANDOM_STRING}" resume:local &&
    docker cp "resume-${RANDOM_STRING}:/app/Resume.pdf" . &&
    docker cp "resume-${RANDOM_STRING}:/app/resume.html" .
