#!/usr/bin/python3
#! -*- coding:utf-8 -*-

"""
DevStation
==========

Headlines

* we create a config / build directory under ~/.devstation
* we read config from there
* we write the prepared DockerFIles to there




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


# commands


### rebuild 
# docker build --tag <tagname>
# We want to be able to have multiple tagged workstations, and use a specific one
# mostly we should use one as a default, and a second as a tryout version for upgrades and
# changes
# As such we need a config file for 

### rebuild *does* require python 3, and docopt.  So its
# homebrew for apple - thats ok
# pip install for rest of the world

login/again
ssh -X pbrian@127.0.0.1 -p 2222

startdev
sudo docker kill run_wkstn
cd projects/workstation
sudo sh build/run.sh
sleep 10
sh build/login.sh

run

sudo docker container prune -f
sudo docker run -d \
 -v ~/data:/var/data \
 -v ~/projects:/var/projects \
 -v ~/secrets:/var/secrets:ro \
 -v ~/Dropbox:/var/Dropbox \
 --name run_wkstn \
 --device /dev/snd \
 -p 2222:22 \
 workstation:latest

"""
##### imports ##### 
import logging, sys
from docopt import docopt
import subprocess
import time
import os
import json

from mikadolib.common import config

##### Module setup #####
# TODO: split out logging into common module
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
log.addHandler(handler)

#: usage defintons
DOCOPT_HELP = """devstation 

Usage:
    devstation.py config 
    devstation.py start (latest | next) 
    devstation.py login (latest | next)
    devstation.py rebuild (latest | next)
    devstation.py status 
    devstation.py makeDockerfile 
    devstation.py runtests
    devstation.py (-h | --help )

Options:
    -h --help    Show this screen

"""

############### Config
LATEST = 'latest'
NEXT   = 'next'
# This is a 'well-known' location
CONFIGLOCATION = os.path.join(os.path.expanduser('~'), 
                              '.devstation/config.ini')

#: pull out into a dedicated config file??
CONFD = config.read_ini(CONFIGLOCATION)['default']
### This is ... fragile
### we are extracting json string from config and parsing here...
unparsedjsonstring = CONFD['volumes']
d = json.loads(unparsedjsonstring)
CONFD['volumes'] = d
for k,i in CONFD.items():
    if "~/" in i:
        CONFD[k] = os.path.join(os.path.expanduser('~'),
                                CONFD[k].replace("~/",""))

def build_sshcmd():
    """ """
    return 'ssh -X {username}@{localhost} -p {ssh_port}'.format(**CONFD)

def build_dockerrun(latest=True):
    """ 
    
    tagname of image
    name of running instance
    """
    _latest = LATEST if latest else NEXT
    instance_name = 'run_{}_{}'.format(CONFD['instance_name'], _latest)
    image_name = '{}:{}'.format(CONFD['tagname'], _latest)
    vols = ''
    for hostpath, mountpath in CONFD['volumes'].items():
        vols += "-v {}:{} ".format(hostpath, mountpath)
    
    return ["sudo docker container prune -f",
            f"sudo docker kill {instance_name}",
    """sudo docker run -d \
        {vols} \
        --name {instance_name} \
        --device /dev/snd \
        -p {ssh_port}:22 \
        {tagname}:{_latest}
    """.format(vols=vols,
               instance_name=instance_name,
               ssh_port=CONFD['ssh_port'],
               _latest=_latest,
               tagname=CONFD['tagname'])]

def build_docker_build(latest=True):
    """Return command to (re)build the container.

    """
    tmpl = 'sudo docker build -t {tagname}:{tagtag} -f {pathtodockerfile}'
    _latest = LATEST if latest else NEXT
    pathtodockerfile = os.path.join(CONFD['devstation_config_root'], 'Dockerfile'+'.'+_latest)
    return tmpl.format(tagname=CONFD['tagname'],
                       tagtag=_latest,
                       pathtodockerfile=pathtodockerfile
                       )
    

def spawn_sibling_console():
    """This script is best thought of as a launcher for other shells we
    shall be working in.  We want to interact with the console, not
    this script much.

    I have played with fork'ing a child console, then passing `fd`
    0,1,2 over to it.  But the easiest way seems to be to assume this
    is a GUI workstation, and people are using a terminal program
    (like Konsole) - so we just spawn konsole and run -e

    """

    sshcmd = '{} {} &'.format(CONFD['terminal_command'],
                              build_sshcmd())
    subprocess.run(sshcmd,
                   shell=True)
        
def show_config(confd=None):
    """Display the current config settings

    >>> show_config({'foo': 'bar'})
    foo : bar
    <BLANKLINE>

    """
    confd = confd or CONFD # for easy testing
    s = ''
    for key, item in confd.items():
        s += '{} : {}\n'.format(key, item)
    print(s)



def handle_start(args):
    log.debug("`start` command passed with args %s", args)
    #do start up here
    cmds = build_dockerrun()
    for cmd in cmds:
        print(cmd)
        time.sleep(10) # brute force give docker time to complete its stuff. 
        #TODO get better solution
        subprocess.run(cmd,
                       shell=True)
    time.sleep(10) #As above    
    handle_login(args)
    
def handle_config(args):
    log.debug("`config` command passed with args %s", args)
    show_config()

def handle_login(args):
    log.debug("`login` command passed with args %s", args)
    spawn_sibling_console()
    
def handle_rebuild(args):
    log.debug("`rebuild` command passed with args %s", args)
    print(build_docker_build(latest=args['latest']))
    
def handle_status(args):
    log.debug("`status` command passed with args %s", args)
    print("To Be Done")

def handle_tests(args):
    from pprint import pprint as pp
    print("\n### Quick Testing - args\n")
    pp(args)
    print("\n### Output of build_dockerrun()\n")
    print(build_dockerrun())
    print("\n### Output of build_docker_build\n")
    pp(build_docker_build())
    print("\n### Output of build_sshcmd()\n")
    pp(build_sshcmd())
    show_config()

    #runtests()
    
def handle_unknown():
    print("Unknown request please type `devstation --help`")

def handle_makeDockerfile():
    makeDocker(latest=True)
    
def makeDocker(latest=True):
    """Take a .skeleton file, and replace defined markup with contents of txt files

    Based on 'dockerfile.skeleton', replace any instance of 
    {{ python }} with the contents of file `templates\python.template`
    
    This is an *extremely* simple templating tool."""

    _latest = LATEST if latest else NEXT
    folder = os.path.join(CONFD['devstation_config_root'],
                          '.build', 'templates')
    skeleton = 'dockerfile.skeleton'
    pathtodockerfile = os.path.join(CONFD['devstation_config_root'],
                                    '.build', 'Dockerfile' + '.' + _latest)
    outputs = ''
    with open(os.path.join(folder, skeleton)) as fo:
        for line in fo:
            if line.find("{{") == 0:
                 file = line.replace("{{","").replace("}}","").strip()
                 filepath = os.path.join(folder, file+".template")
                 txt = open(filepath).read()
                 outputs += "\n### {}\n{}\n".format(line, txt)
            else:
                 outputs += "{}".format(line)
    fo = open(pathtodockerfile, 'w')
    fo.write(outputs)
    fo.close()


def run(args):

    if args['config']:
        handle_config(args)
    elif args['start']:
        handle_start(args)
    elif args['login']:
        handle_login(args)
    elif args['rebuild']:
        handle_rebuild(args)
    elif args['status']:
        handle_status(args)
    elif args['runtests']:
        handle_tests(args)
    elif args['makeDockerfile']:
        handle_makeDockerfile()
    else:
        handle_unknown()
        

def runtests():
    import doctest
    doctest.testmod()

def main():
    args = docopt(DOCOPT_HELP)
    run(args)

if __name__ == '__main__':
    main()
