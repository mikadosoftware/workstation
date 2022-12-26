#! /bin/bash

#python3 immutableworkstation3.py createDockerfile --templatedir=/home/pbrian/projects/docker_vnc_immutable/templates

tagname="mikado-immutableworkstation"
path2dockerfile="/home/pbrian/projects/docker_vnc_immutable/Dockerfile"
path2contextdir="/home/pbrian/projects/docker_vnc_immutable/"
podman build -t ${tagname} -f ${path2dockerfile}  ${path2contextdir}  --squash
