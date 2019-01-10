===========================
Docker Workstation Anywhere
===========================

The concept of an *immutable server* for production deployment is now
fully mainstream, but the same concepts underpinning servers is less
applied to the workstations on which the developers work.

We have a tendancy to start with a nice clean laptop, a Mac if we are
lucky, and slowly but surely *stuff* creeps on, dependancies we did
not know about appear and we stop trusting the platform we stand on.

So I have used Docker to make my own *immutable workstation*.  It
means that I get *exactly* the same stack running on my
banged-about-on-commute laptop, my wife's nice big screen iMac and
even on my client's Windows box, that I had to use for client's policy
reasons.  So wherever I was, I was using the same config of emacs -
using it on a windows machine or a mac or a linux host, it was the
same emacs, and the same nice set of tools like grep.  And it was
running XWindows in those places too.

Secondly, I get the ratchet effect of continuously improving security
- I can always improve something on the install, and just rerun
`docker build` and I have permanently remebered to fix that security
hole wherever I build my workstation.

I use X-Forwarding to run the same visual tools, configured the same
way, on any box I am working on, and *anything* that changes I keep in
source control (here in this repo) and my secrets are all stored on a USB key that I carry with me and plugin to the host - so my github ssh key is on a USB stick, that when I plug it in, .
    

Using X Windows
===============

The *essential* parts of this approach are hard to dig out from Google
searches, but I hope this makes them clearer - the below code will
produce a working local docker instance, ssh into it and display an
app *from* docker but *on* the host desktop.

We build a X11 capable docker image ::

    FROM ubuntu:18.04
    
    RUN apt-get update && \
        apt-get install -y openssh-server \
                           x11-apps                       

    RUN mkdir -p /var/run/sshd                     
    RUN echo 'root:root' | chpasswd 
    RUN sed -ri 's/^#PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
    RUN sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config
    RUN sed -ri 's/^#AllowTcpForwarding\s+.*/AllowTcpForwarding yes/g' /etc/ssh/sshd_config
    RUN sed -ri 's/^#X11Forwarding\s+.*/X11Forwarding yes/g' /etc/ssh/sshd_config
    RUN sed -ri 's/^#X11UseLocalhost\s+.*/X11UseLocalhost no/g' /etc/ssh/sshd_config

    EXPOSE 22
    CMD ["/usr/sbin/sshd", "-D"]

We then build the above image::

    # sudo docker build -t devbox:latest .

Now run it, listening on the localhost port of 2222, which is then mapped to 22 on the container
::

    # docker run -d  --name devbox-live -v /data/projects:/projects -p 2222:22 devbox:latest
    
we should now have a running container listening on port 2222

So we can ssh tunnel into the container using::

    # ssh -X root@localhost -p 2222

There may be some faffing with .XAuthority files. Ignore that for now.
But we should then be able to run ::

   # xeyes 

on the container, and it will appear on the laptop we are running on.

#TODO: screenshot 

Using Sound
===========

There is a developer who (I think) works for Docker and has a list of YouTube
videos showing how to do things like run Skype on Docker.  She developed a
`snd` device parameter for `docker run`, which seems to work fine. I don't do
much with it but should expand on it.  

Using Secrets
=============


/etc/fstab on host machine::


    # /etc/fstab: static file system information.
    ....
    UUID=ed74f120-1736-4f59-8752-06098a635c16 /home/pbrian/secrets/usb   ext4  user,rw,auto,nofail  0   0	
    ...

    I used `sudo blkid` to get the UUID for that specific USB key.
    
    It is then automounted to my home dir, where docker will make it
    visible in the docker instance, and I get to use the ssh keys on
    the USB stick to authenticate to, for example, github.

Using Dropbox
=============

I have some files I keep on private github repos, but for most documents
(things like Bank statements) it seems easier to just store them on Dropbox.
I merely have my Dropbox folder on my home dir, and mount it into Docker.
It seems to work with no horrible clashes so I will keep it. At somepoint it
seems sensible to migrate to having the Dropbox client actually running on
the docker instance.

Its not terribly secure, but it seems good enough.

Why is this good?
-----------------

Quite simply, I can easily control the dev environment, rebuild it at
will, and run programs "on my latop" when they are not installed or
configured on the laptop.

In fact I think the best part of this is configuration for my *whole*
dev machine is sgtored on github, and can be re-created anywhere
easily.

With the volume mounted, I can then use emacs / konsole running inside
a container, and adjust files that are stored on my local laptop.

I then have a consistent dev environemnt 

Also, I can easily reuild it

Also I can spin up a microservice on laptop that also points at the
same volume, and it will thus be using the code I just developed

This works even if I change underlying OS - which is good for
wandering contractors like me.

TODO::

  #TODO:: allow two workstations on same host, so I can play / verify changes
  #TODO:: get dropbox installed on docker instance


