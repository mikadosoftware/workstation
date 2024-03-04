#! /bin/bash

logfile="this.log"
tagname="myworkstation"
path2dockerfile="`pwd`/Dockerfile"
path2contextdir="`pwd`/DockerContextDir"
podman build -t ${tagname} -f ${path2dockerfile}  ${path2contextdir}  --squash --logfile=${logfile}
