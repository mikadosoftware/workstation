=====================
ImmutableWorkstation
=====================

Intro
=====


The concept of an *immutable server* for production deployment is now
fully mainstream, but the same concepts underpinning servers is less
applied to the workstations on which the developers work.

We have a tendency to start with a nice clean laptop, a Mac if we are
lucky, and slowly but surely *stuff* creeps on, dependencies we did
not know about appear and we stop trusting the platform we stand on.

So I have used Docker to make my own *immutable workstation*.  It
means that I get *exactly* the same stack running on my
banged-about-on-commute laptop, my wife's nice big screen iMac and
even on my client's Windows box, that I had to use for client's policy
reasons.  So wherever I was, I was using the same config of emacs -
using it on a windows machine or a mac or a Linux host, it was the
same emacs, and the same nice set of tools like grep.  And it was
running XWindows in those places too.

Secondly, I get the ratchet effect of continuously improving security
- I can always improve something on the install, and just rerun
`docker build` and I have permanently remembered to fix that security
hole wherever I build my workstation.

I use X-Forwarding to run the same visual tools, configured the same
way, on any box I am working on, and *anything* that changes I keep in
source control (here in this repo) and my secrets are all stored on a
USB key that I carry with me and plugin to the host - so my GitHub ssh
key is on a USB stick, that when I plug it in, .
    

Documentation can be found at https://workstation.readthedocs.io/en/latest/

::

    `immutableworkstation` can create docker images from config, and
    launch those images so that as a developer you can work inside the
    container, but using X-applications on the host laptop.

    So you can define your workstation in code, but take it with you
    from laptop to home to work.



Getting Started
===============

Firstly install the python (3) package on your machine::

    sudo pip install immutableworkstation

First run:

    $ immutableworkstation.py

    Usage:
	immutableworkstation.py quickstart

You will need to follow the instructions on setting up
config. Basically we need config stored in your local home dir in
`.immutableworkstation`.  This will be the tempaltes etc to configure
docker.  The only way to do this right now is copy from the example
set in github. At some point I hope to improve the quickstart


After config has been set up ::

    $ immutableworkstation.py

    Usage:
	immutableworkstation.py config 
	immutableworkstation.py start (latest | next) 
	immutableworkstation.py stop (latest | next) 
	immutableworkstation.py login (latest | next)
	immutableworkstation.py buildDocker (latest | next)
	immutableworkstation.py next2last
	immutableworkstation.py status
	immutableworkstation.py quickstart
	immutableworkstation.py (-h | --help )

    Options:
	-h --help    Show this screen


Daily use case
--------------

So to start a fresh docker instance we use::

    immutableworkstation.py start next

THis will boot up docker and throw you a ssh login

We can also open a new terminal into the same docker::

    immutableworkstation.py login next

And stop it ::

    immutableworkstation.py stop next



Configuration
-------------

Initially `immutableworkstation.py` can run without a config folder,
but pretty much the only thing you can do is `quickstart` which 
will help setup a local config folder.

The example local config folder is stored in the python package and
deployed to your machine as a data file.  When we run `quickstart` we
deploy that to `~\.immutableworkstation\` folder in your homedir

This has

* a config.ini file
* a `.latest` folder holding the templates to build "latest" Dockerfile
* a `.next` folder holding the templates to build the "next" Dockerfile

Config file is located as `~/.immutableworkstation/config.ini`
It has following format and items ::

    [default]
    tagname   = workstation
    instance_name =immutableworkstation
    localhost  = 127.0.0.1
    username   = pbrian
    ssh_port   = 2222
    devstation_config_root = ~/.immutableworkstation
    terminal_command = /usr/bin/konsole -e
    volumes = {"~/data":     "/var/data",
               "~/projects": "/var/projects",
               "~/secrets":  "/var/secrets:ro",
               "~/Dropbox":  "/var/Dropbox"
               }



`volumes` is a json-formatted string that will be converted during config
reading.
`tagname` is the tagname used to identify the docker *instance*
`image_name` is the name used to identify the built docker image, from
    which we will run an instance.  You must build a docker instance.
`localhost` is obvious, probably needs to be removed
`username` is the name of the (only?) user who will use the docker instance.
As it is the only name and user that password is set to that as well.

`ssh_port` port for docker instance to listen on for ssh connections 
   from the host machine (how we talk to our dev machine)
`devstation_config_root` the location of the config file, plus other templates
`terminal_command` - command to run before sshing to the running docker instance
I am assuming you have `konsole`. if not adjust the config.

This will have files for the config ready to install - they will be
place on '/usr/local/config' (TODO: rename that location to branded).::

    $ immutableworkstation.py quickstart

You will be asked at least one question
    
Preparing a dockerfile
----------------------
TBD

Getting started
---------------

1. Set up config - see above
2. Make a docker file
3. Build a Docker image





we are targetting windows, linux and apple machines so will need
sensible simple scripts else the start up and try me out barrier will
be too high.  however having python scripts makes the development part
waaay easier, and the templating is all in python anyhow, so I think
we have to have some road bumps.  I think anone wanting to try this
out is going to be capable of installing py3 anyway.  Our target
demographic is developers who want more control.

I am building a one-stop shop developer machine on Docker which means
it is a large Dockerfile - which is becoming unwieldy So I shall have
a template folder, which will hold

`dockerfile.skeleton` This is the bones of the Dockerfile, with very
simple replace-locations built in such as::

    FROM ubuntu:18.04
    ENV USERHOME /home/pbrian

    {{ apt }}
    ^^^^^^^^^^^^^^^^^
    this bit will get replaced with contents of `apt.template`

Constraints are that the {{ file }} must be on its own line, with only
spaces between it and line start / end It is NOT using Jinja2, it just
looks like it. Because one day it might.

Its that simple. We can play around with variables if we really need to.



Building Next and Last
----------------------

The idea is that I think of something I should have added to my workstation
such as a python package in `requirements.txt` or some .deb file.

I go to ~/.immutableworkstation - where the .next and .latest copies of
the config is kept.  I change say the requirements.txt file in .next then I
rebuild docker image for next::

   $ immutableworkstation.py buildDocker next

Then I can try that out ::

   $ immutableworkstation.py start next

If all is good I can prep it for my next go with latest::

   $ immutableworkstation.py next2last

   (this will move the old .latest files and replace them with
   .next. You will be prompted)

   $ immutableworkstation.py buildDocker latest

   Now we can `start latest` again
