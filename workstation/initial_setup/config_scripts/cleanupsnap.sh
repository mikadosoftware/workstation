#!/bin/bash

sudo snap set system refresh.retain=2

 #Removes old revisions of snaps
 #CLOSE ALL SNAPS BEFORE RUNNING THIS
 set -eu
 LANG=en_US.UTF-8 snap list --all | awk '/disabled/{print $1, $3}' |
     while read snapname revision; do
         sudo snap remove "$snapname" --revision="$revision"
     done

sudo apt-get clean
sudo apt-get autoremove --purge
sudo apt install bleachbit
sudo flatpak uninstall --unused

