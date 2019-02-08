#! -*- coding:utf-8 -*-
"""

we are targetting windows, linux and apple machines so will need
sensible simple scripts else the start up and try me out barrier
will be too high.  however having python scripts makes the
development part waaay easier, and the templating is all in python
anyhow, so I think we have to have some road bumps.  I think anone
wanting to try this out is going to be capable of installing py3
anyway.  Our target demographic is developers who want more
control.



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

##### Module setup #####
# TODO: split out logging into common module
log = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
log.addHandler(handler)


############### Config
# TODO: split out into proper config (common module)
tag_latest = 'devstation_latest'
tag_next   = 'devstation_next'
localhost  = '127.0.0.1'
username   = 'pbrian'
ssh_port   = '2222'
volumes    = [
              ['~/data', '/var/data'],
              ['~/projects', '/var/projects'],
              ['~/secrets', '/var/secrets:ro'], #TODO: special case this elsewhere
              ['~/Dropbox', '/var/Dropbox']
             ]

CONFD = {'tag_latest': tag_latest,
          'tag_next': tag_next,
          'localhost': localhost,
          'username': username,
          'ssh_port': ssh_port,
          'volumes': volumes,
          'terminal_command': 'konsole -e'
          }


def build_sshcmd():
    """ """
    return 'ssh -X {username}@{localhost} -p {ssh_port}'.format(**CONFD)

def build_dockerrun():
    """ """
    return ["""sudo docker container prune -f""",
            "sudo docker kill run_wkstn",
    """sudo docker run -d \
        -v ~/data:/var/data \
        -v ~/projects:/var/projects \
        -v ~/secrets:/var/secrets:ro \
        -v ~/Dropbox:/var/Dropbox \
        --name run_wkstn \
        --device /dev/snd \
        -p 2222:22 \
        workstation:latest
    """]


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


#: usage defintons
DOCOPT_HELP = """devstation 

Usage:
    devstation.py config 
    devstation.py start (latest | next) 
    devstation.py login (latest | next)
    devstation.py rebuild (latest | next)
    devstation.py status 
    devstation.py runtests
    devstation.py (-h | --help )

Options:
    -h --help    Show this screen

"""

def handle_start(*args):
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
    handle_login()
    
def handle_config(*args):
    log.debug("`config` command passed with args %s", args)
    show_config()

def handle_login(*args):
    log.debug("`login` command passed with args %s", args)
    spawn_sibling_console()
    
def handle_rebuild(*args):
    log.debug("`rebuild` command passed with args %s", args)

def handle_status(*args):
    log.debug("`status` command passed with args %s", args)
    print("To Be Done")

def handle_unknown():
    print("Unknown request please type `devstation --help`")

    

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
        runtests()
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
