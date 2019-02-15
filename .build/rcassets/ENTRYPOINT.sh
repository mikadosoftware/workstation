#!/bin/bash

## THis is run *inside* new docker instnce, but has mounted the
## secrets volume

SECRETS_VOL="/var/secrets/usb"
cp -r $SECRETS_VOL/.ssh/* /home/pbrian/.ssh

chown -R pbrian:pbrian /home/pbrian/
chown -R pbrian:pbrian /home/pbrian/.ssh
chmod -R 0700 /home/pbrian/.ssh
 
###
mkdir /home/pbrian/.aws
cp -r $SECRETS_VOL/aws-credentials /home/pbrian/.aws/credentials
chmod 0777 -R /home/pbrian/.aws

## Add local tools
cd /var/projects/mkrepo
python setup.py install
cd /var/projects/todoinator
python setup.py install

#Now finally start this ready for XForwarding
/usr/sbin/sshd -D
