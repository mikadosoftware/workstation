===========================
Docker Workstation Anywhere
===========================

tl;dr
=====

`sh rebuild-rerun.sh` will build dockerfile locally, and run the docker
locally and log me in via ssh. I can then use X commands as needed.




Using Docker as run-anywhere developer environment
==================================================

One of the basic principles of running software in production is to be
clear and precise about the software and versions on top of which ones
code will be running.  This also is true for the *workstation* on
which one *develops* the code - I think it is crazy to just accept
whatever happens to be on a given distro.

So enter Docker.  We can spin up a plain old distro on our laptop, and
*then* build a new Docker instance of the exact perfect developer
machine we want.  On top of this we can then use ssh and X-Forwarding
to have a X-ready app (such as an IDE, or web browser) run on the
ideal machine, but have the X portion appear on our desktop.

This means we can build the perfect environment and run it on any
location.

I have used this approach on Linux laptops & Windows desktops, giving
me a consistent developer environment plus access to Linux tools even
on a non-Linux OS.


The bare bones
==============

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

This works even if I change underlying OS - which is good for wandering
contractors like me.

