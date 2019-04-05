#!/usr/bin/python3
#! -*- coding:utf-8 -*-

"""
DevStation
==========

This is a single entry point for the `devstation` project.

The project is pretty simple - I want to have a consistent, immutable
workstation on any host machine I am developing on - so I am using a
docker instance on a host machine - the instance is my development
"machine", and it can be rebuilt from consistent templates - this
script helps control all that - its supposed to be easier to get
started than a bunch of poorly documneted shell scripts.

* the start and stopping of the dev instance.
* the compilation of the docker image 
* vsarious config and templates used to build to docker image.

This script does quite a lot, and needs to be installed on 
the host machine - do so using

   pip3 install docopt
   python3 setup.py install
   (I will launch it on PyPI soon)

Once this is done, you should be able to run 

  ./immutableworkstation.py

And see the help options::

    Usage:
        immutableworkstation.py config 
        immutableworkstation.py start (latest | next) 
        immutableworkstation.py login (latest | next)
        immutableworkstation.py rebuild (latest | next)
        immutableworkstation.py status 
        immutableworkstation.py makeDockerfile 
        immutableworkstation.py runtests
        immutableworkstation.py quickstart
        immutableworkstation.py (-h | --help )

    Options:
        -h --help    Show this screen


Configuration
-------------

Initially `immutableworkstation.py` can run without a config folder,
but pretty much the only thing you can do is `quickstart` which 
will help setup a local config folder.

we have a ~\.devstation\ folder in homedir
This has

* a config.ini file
* a `.latest` folder holding the templates to build "latest" Dockerfile
* a `.next` folder holding the templates to build the "next" Dockerfile

A helper script to build config will be needed shortly.
TODO: build clean docker for testing script install on

Config file is located as `~/.devstation/config.ini`
It has following format and items ::

    [default]
    tagname   = workstation
    instance_name = devstation
    localhost  = 127.0.0.1
    username   = pbrian
    ssh_port   = 2222
    devstation_config_root = ~/.devstation
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
`username` is the name of the (only?) user who will use the docker instace.
`ssh_port` port for docker instance to listen on for ssh connections 
   from the host machine (how we talk to our dev machine)
`devstation_config_root` the location of the config file, plus other templates
`terminal_command` - command to run before sshing to the running docker instance


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


Using latest and next
pip install black as an example

[ ] put blog.mikadosoftware onto AWS and run this testing with docker on it.
[ ] migrate rest of the articles there.

[ ] create a plain docker instance and just import devstation, see if it works (ie clean install)



[ ] run todoinator over this and all my projects
[ ] run the get github projects into one place 
[ ] this is looking like a personal workstation setup thingy - immutable workstation, todos, gitgetter
[ ] launch tester docker with access to this projects so can pip -e, then 
    ensure it can build locally the config etc correctly.

"""
##### imports #####
import logging, sys
from docopt import docopt
import subprocess
import time
import os
import json
from pprint import pprint as pp
from mikado.core import config

##### Module setup #####
# TODO: split out logging into common module
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
log.addHandler(handler)

DRYRUN = False

#: usage defintons
DOCOPT_HELP = """devstation 

Usage:
    immutableworkstation.py config 
    immutableworkstation.py start (latest | next) 
    immutableworkstation.py stop (latest | next) 
    immutableworkstation.py login (latest | next)
    immutableworkstation.py buildDocker (latest | next)
    immutableworkstation.py makeDockerfile (latest | next)
    immutableworkstation.py status
    immutableworkstation.py quickstart
    immutableworkstation.py (-h | --help )

Options:
    -h --help    Show this screen

"""

DOCOPT_HELP_SHORT = '''We cannot detect a conifg folder at ~/.devstation - quickstart to create

Usage:
    immutableworkstation.py quickstart 

 '''

############### Config
LATEST = "latest"
NEXT = "next"
# This is a 'well-known' location
CONFIGDIR      = os.path.join(os.path.expanduser("~"), ".devstation")
CONFIGLOCATION = os.path.join(os.path.expanduser("~"), ".devstation/config.ini")

#: pull out into a dedicated config file??
def read_disk_config():
    try:
        confd = config.read_ini(CONFIGLOCATION)["default"]
        ### This is ... fragile
        ### we are extracting json string from config and parsing here...
        unparsedjsonstring = confd["volumes"]
        d = json.loads(unparsedjsonstring)
        confd["volumes"] = d
        for k, i in confd.items():
            if "~/" in i:
                confd[k] = os.path.join(os.path.expanduser("~"), confd[k].replace("~/", ""))
                hasconfigdir=True
    except:
        confd = {}
        hasconfigdir=False
    return confd, hasconfigdir

def write_disk_config(confd):
    """ """
    config.write_ini(confd, CONFIGLOCATION)
    

CONFD, HASCONFIGDIR = read_disk_config()

def build_sshcmd():
    """ """
    return "ssh -X {username}@{localhost} -p {ssh_port}".format(**CONFD)


def build_dockerrun(latest=True):
    """ 
    
    tagname of image
    name of running instance
    """
    _latest = LATEST if latest else NEXT
    instance_name = "run_{}_{}".format(CONFD["instance_name"], _latest)
    image_name = "{}:{}".format(CONFD["tagname"], _latest)
    vols = ""
    for hostpath, mountpath in CONFD["volumes"].items():
        vols += "-v {}:{} ".format(hostpath, mountpath)

    return [
        "sudo docker container prune -f",
        f"sudo docker kill {instance_name}",
        """sudo docker run -d \
        {vols} \
        --name {instance_name} \
        --device /dev/snd \
        -p {ssh_port}:22 \
        {tagname}:{_latest}
    """.format(
            vols=vols,
            instance_name=instance_name,
            ssh_port=CONFD["ssh_port"],
            _latest=_latest,
            tagname=CONFD["tagname"],
        ),
    ]


def build_docker_build(latest=True):
    """Return command to (re)build the container.

    We store the Dockerfile (as that name)
    in dir .next or .latest so that we can 
    have various templates and assets and so on
    in the 'context' directory.

    """
    tmpl = "sudo docker build -t {tagname}:{tagtag} {pathtodockerfile}"
    _latest = LATEST if latest else NEXT
    pathtodockerfile = os.path.join(CONFD["devstation_config_root"], "." + _latest)
    return tmpl.format(
        tagname=CONFD["tagname"], tagtag=_latest, pathtodockerfile=pathtodockerfile
    )


def run_subprocess(cmd):
    """ """
    if DRYRUN:
        print(cmd)
    else:
        subprocess.run(cmd, shell=True)


def spawn_sibling_console():
    """This script is best thought of as a launcher for other shells we
    shall be working in.  We want to interact with the console, not
    this script much.

    I have played with fork'ing a child console, then passing `fd`
    0,1,2 over to it.  But the easiest way seems to be to assume this
    is a GUI workstation, and people are using a terminal program
    (like Konsole) - so we just spawn konsole and run -e

    """

    sshcmd = "{} {} &".format(CONFD["terminal_command"], build_sshcmd())
    log.debug(sshcmd)
    run_subprocess(sshcmd)


def show_config(confd=None):
    """Display the current config settings

    >>> show_config({'foo': 'bar'})
    foo : bar
    <BLANKLINE>

    """
    confd = confd or CONFD  # for easy testing
    s = ""
    for key, item in confd.items():
        s += "{} : {}\n".format(key, item)
    print(s)


def handle_start(args):
    # do start up here
    cmds = build_dockerrun(args["latest"])
    for cmd in cmds:
        # TODO get better solution
        print(cmd)
        subprocess.run(cmd, shell=True)
        time.sleep(2)  # brute force give docker time to complete its stuff.
    time.sleep(10)  # As above, but let docker catch up before login
    handle_login(args)


def handle_config(args):
    show_config()


def handle_login(args):
    spawn_sibling_console()


def handle_buildDocker(args):
    """Trigger the processes to create new dockerfile and then build image. """
    makeDocker(latest=args["latest"])
    cmd = build_docker_build(latest=args["latest"])
    run_subprocess(cmd)


def handle_status(args):
    """Show container status. """
    cmd = 'sudo docker container ls'
    run_subprocess(cmd)

def handle_stop(args):
    """Kill the specified instance. """
    _latest= LATEST if args["latest"] else NEXT
    #: rewrite so this is not in two places
    instance_name = "run_{}_{}".format(CONFD["instance_name"], _latest)
    cmd = 'sudo docker container kill {}'.format(instance_name)
    run_subprocess(cmd)
    
def hasValidConfig():
    """This is a placeholder for future development on checking curr env. """
    has_config_file = os.path.isfile(CONFIGLOCATION)
    return all([has_config_file])

import shutil
def gatherinfo():
    questions = {'username': 'What username should be the default (only) on your immutable workstation?',
                }
    answers = {}
    for label, question in questions.items():
        answer = input(question)
        answers[label] = answer
    return answers

def handle_quickstart(args):
    """From pacakge data files copy into this users local dir.

    ALso adjust config based on questions asked of user in
    sphinx_quickstart style

    """
    helpmsg = ''
    if hasValidConfig():
        helpmsg += """You appear to have an existing config in {}.  
                      Please adjust it manually - view docs for
        help.""".format(CONFIGLOCATION)
    if not hasValidConfig():
        helpmsg += "We shall walk you thorugh a series of questions"
        answersd = gatherinfo()
        try:
            shutil.copytree('/usr/local/config/', CONFIGDIR)
        except Exception as e:
            print(e)
            raise
        
        #now lets update the config file
        confd, hasconfigdir = read_disk_config()
        confd.update(answersd) # !!!!
        write_disk_config(confd)
        print("We have adjusted the config file at {} with your answers. Please check".format(CONFIGLOCATION))

def handle_unknown():
    print("Unknown request please type `devstation --help`")


def handle_makeDockerfile(args):
    makeDocker(latest=args["latest"])

    
def makeDocker(latest=True):
    """Take a .skeleton file, and replace defined markup with 
       contents of txt files

    Based on 'dockerfile.skeleton', replace any instance of 
    {{ python }} with the contents of file `templates\python.template`
    
    This is an *extremely* simple templating tool.  It is *not*
    supposed to have the complexity even of Jinja2.  Its supposed to 
    be really dumb.  Lucky I wrote it then :-).


    """

    _latest = "."+LATEST if latest else "."+NEXT
    current_folder = os.path.join(CONFD["devstation_config_root"], _latest)
    templates_folder = os.path.join(current_folder, 'templates') 
    pathtodockerfile = os.path.join(current_folder, 'Dockerfile')
    skeleton = "dockerfile.skeleton"
    outputs = ""
    with open(os.path.join(templates_folder, skeleton)) as fo:
        for line in fo:
            if line.find("{{") == 0:
                file = line.replace("{{", "").replace("}}", "").strip()
                filepath = os.path.join(templates_folder, file + ".template")
                txt = open(filepath).read()
                outputs += "\n### {}\n{}\n".format(line, txt)
            else:
                outputs += "{}".format(line)
    fo = open(pathtodockerfile, "w")
    fo.write(outputs)
    fo.close()
    telluser("Written new Dockerfile at {}".format(pathtodockerfile))
    
def telluser(msg):
    print(msg)

def run(args):

    #: start with quickstart as it may be our only options
    #: [ ] make this safer with .get 
    if args["quickstart"]:
        handle_quickstart(args)
    elif args["config"]:
        handle_config(args)
    elif args["start"]:
        handle_start(args)
    elif args["login"]:
        handle_login(args)
    elif args["buildDocker"]:
        handle_buildDocker(args)
    elif args["makeDockerfile"]:
        handle_makeDockerfile(args)
    elif args["status"]:
        handle_status(args)
    elif args["stop"]:
        handle_stop(args)
    else:
        handle_unknown()


def runtests():
    import doctest
    doctest.testmod()


def main():
    
    ## if we have not quickstart'd the config dir, only show quickstart option.
    if HASCONFIGDIR:
        args = docopt(DOCOPT_HELP)
    else:
        args = docopt(DOCOPT_HELP_SHORT)
    run(args)


if __name__ == "__main__":
    main()
