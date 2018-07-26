===========================
Docker Workstation Anywhere
===========================

The concept of an *immutable server* for prodiction deployment is now
fully mainstream, but the same concepts underpinning servers is less
applied to the workstations on which the developers work.

We have a tendancy to start with a nice clean laptop, a Mac if we are
lucky, and slowly but surely *stuff* creeps on, dependancies we did
not know about appear and we stop trusting our main tool.

So I have used Docker to make my own "immutable" workstation.  It is the same
stack running on my banged-about-on-commute laptop, my wife's nice big screen iMac
and even on my client's Windows box, that I had to use for policy reasons.

I use X-Forwarding to run the same visual tools, configured the same way, on
any box I am working on, and *anything* that changes I keep in source control
(or on a secure key).

This workstation has a few rules

* The build is automated - no manual steps involved.
* I have to be able to precisely define what is on there and how it is configured.
* I have to be able to re-create it exactly
* If I restart, all state is reset (this is not as crazy as it sounds)
* It needs to be secure




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

