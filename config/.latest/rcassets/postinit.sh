#!/bin/bash

## THis is run *inside* new docker instnce, but has mounted the secrets volume

# must not be in docker
SECRETS_VOL="/var/secrets/usb"
cp -r $SECRETS_VOL/.ssh/* ~/.ssh
chmod -R 0600 ~/.ssh
