#!/bin/bash

## THis is run *inside* new docker instnce, but has mounted the
## secrets volume

SECRETS_VOL="/var/secrets/usb"
cp -r $SECRETS_VOL/.ssh/* /home/pbrian/.ssh

chown -R pbrian:pbrian /home/pbrian/
chown -R pbrian:pbrian /home/pbrian/.ssh
chmod -R 0700 /home/pbrian/.ssh
 
# add aws credentials from host to docker
mkdir /home/pbrian/.aws
chmod 0622 -R /home/pbrian/.aws
cp -r $SECRETS_VOL/aws-credentials /home/pbrian/.aws/credentials

# add github 'hub' credentials from host to here
echo "export GITHUB_TOKEN=`cat /var/secrets/github-token`" >> /home/pbrian/.bashrc


## Add local tools
cd /var/projects/mikado-tools
python3 setup.py install



#: firefox should be run from the docker container so file:// works 
echo "export MOZ_NO_REMOTE=1" >> /home/pbrian/.bashrc
 
#Now finally start this ready for XForwarding
/usr/sbin/sshd -D
