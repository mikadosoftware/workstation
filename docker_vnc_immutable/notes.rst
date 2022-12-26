Migrating to docker vnc
------------------------

UID issues
----------

Mounting volumes.
I dont particularly want to have volumes mounted as 'named volumes' 
(these are a "filesystem" under Docker control, running on top of the host filesystem).

I prefer using `bind mounts`, where the docker instance talks to a host filesystem in the
"normal" manner.  The only problem here is synchronising the UID/GID *numbers* so that the 
host filesystem has privileges for a given host UID, and that the same UID number is assigned 
inside the docker container.

A "cheat" method for this is to start the docker with `userns=keep-id` which ensures that 
the UIDs match.

::

  --volume /home/pbrian/projects:/var/projects  \
  --volume /home/pbrian/secrets:/var/secrets:ro  \
  --volume /home/pbrian/Dropbox:/var/Dropbox  \
  --userns=keep-id \


groupadd --gid 5000 podgroup
(view in /etc/group)

usermod -a -G podgroup pbrian

$ groups pbrian
pbrian : pbrian adm cdrom sudo dip plugdev kvm lpadmin lxd sambashare podgroup

$ sudo chown -R pbrian:podgroup projects/
$ sudo chmod -R 2775 projects/
$ sudo chmod -R 00775 projects/
## will clear the setuid applied by 2.... mayeb we need that for shred directoures


- use userns approach to ensure get same UID both host and docker
- ensure entrypoint can load up secrets usb
- also clear up entrypoints,
- also reduce size of main python script, use ini file or docopt

* tempaltesfile location
* optional dockerfile location
* optional tagnmae, build and launch using vncstart, and launch vncviewer

