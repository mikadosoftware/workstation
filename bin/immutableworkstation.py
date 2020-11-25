#!/usr/bin/python3
#! -*- coding:utf-8 -*-

"""
ImmutableWorkstation
====================

This is a single entry point for the `immutableworkstation` project.

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


[ ] Implement expect-style testing so we can automate testing.
[x] put the home dir into git seperate to rest of pacakge (ie thats the indivudal part)
[ ] put blog.mikadosoftware onto AWS and run this testing with docker on it.
[ ] migrate rest of the articles there.
[x] create a plain docker instance and just import devstation, see if it works (ie clean install)
[ ] run the get github projects into one place 

"""
##### imports #####
import logging, sys
from docopt import docopt
import subprocess
import time
import os
from pprint import pprint as pp
from mikado.core import config
import shutil
import json

##### Module setup #####
# TODO: split out logging into common module
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
log.addHandler(handler)

DRYRUN = False
PDB = False
OCI_CMD = 'sudo docker'
OCI_CMD = 'podman'

#: usage defintons
DOCOPT_HELP = """immutableworkstation

Usage:
    immutableworkstation.py config 
    immutableworkstation.py start (latest | next) [options] 
    immutableworkstation.py stop (latest | next) [options] 
    immutableworkstation.py login (latest | next) [options]
    immutableworkstation.py buildDocker (latest | next) [options]
    immutableworkstation.py next2last
    immutableworkstation.py status
    immutableworkstation.py quickstart
    immutableworkstation.py test
    immutableworkstation.py (-h | --help )


Options:
    -h --help    Show this screen
    -d --dryrun  dryrun

"""

DOCOPT_HELP_SHORT = """immutableworkstation

Usage:
    immutableworkstation.py quickstart

Options:
    -h --help    Show this screen
    -d --dryrun  dryrun

"""

############### Config
LATEST = "latest"
NEXT = "next"
# This is a 'well-known' location
CONFIGDIR = os.path.join(os.path.expanduser("~"), ".immutableworkstation")
CONFIGLOCATION = os.path.join(
    os.path.expanduser("~"), ".immutableworkstation/config.ini"
)
STARTER_CONFIG_URL = "https://github.com/mikadosoftware/immutableworkstation_starter_config/archive/master.zip"

#: pull out into a dedicated config file??
def read_disk_config():
    """

    Volumes - this is tricky to bend .ini files to handle lists of tuples
    The encoded json approach was just too fragile.
    So a new section is being added 
    """
    try:

        confd = config.read_ini(CONFIGLOCATION)
        if confd["devstation_config_root"].startswith("~/"):
            confd["devstation_config_root"] = confd["devstation_config_root"].replace(
                "~", os.path.expanduser("~")
            )
        volumesd = config.read_ini(CONFIGLOCATION)["volumes"]
        #: we want to convert an ini section to a dict.
        confd["volumes"] = {}
        for k, i in volumesd.items():
            if "~/" in k:
                # convert ~/data to /home/user/data
                newkey = os.path.join(os.path.expanduser("~"), k.replace("~/", ""))
                # we should have volumes = {'/home/user/data': '/var/data'}
                confd["volumes"][newkey] = i
                hasconfigdir = True
    except Exception as e:
        log.error("Failed to read config - error is %s", e)
        if PDB:
            import pdb

            pdb.set_trace()
        confd = {}
        hasconfigdir = False
    return confd, hasconfigdir


def write_disk_config(confd):
    """ """
    config.write_ini(confd, CONFIGLOCATION)


CONFD, HASCONFIGDIR = read_disk_config()
if PDB:
    print(CONFD)


def build_sshcmd():
    """Create the command used to connect to running docker via ssh."""

    return "ssh -X {username}@{localhost} -p {ssh_port}".format(**CONFD)


def build_dockerrun(latest=True):
    """create the command used to start docker instance. 
    
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
        "{} container prune -f".format(OCI_CMD),
        """{OCI_CMD} run -d \
        {vols} \
        --name {instance_name} \
        --device /dev/snd \
        -p {ssh_port}:22 \
        {tagname}:{_latest}
    """.format(
            OCI_CMD=OCI_CMD,
            vols=vols,
            instance_name=instance_name,
            ssh_port=CONFD["ssh_port"],
            _latest=_latest,
            tagname=CONFD["tagname"],
        ),
    ]


def build_docker_build(latest=True):
    """Create command used to (re)build the container.

    We store the Dockerfile (as that name)
    in dir .next or .latest so that we can 
    have various templates and assets and so on
    in the 'context' directory.

    """
    tmpl = "{} build -t {{tagname}}:{{tagtag}} {{pathtodockerfile}}".format(OCI_CMD)
    _latest = LATEST if latest else NEXT
    pathtodockerfile = os.path.join(CONFD["devstation_config_root"], "." + _latest)
    return tmpl.format(
        tagname=CONFD["tagname"], tagtag=_latest, pathtodockerfile=pathtodockerfile
    )

def read_subprocess(cmd):
    """Run a command and return output """
    
    result = subprocess.run(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True,
                            shell=True)
    txt = result.stdout
    return txt

    
def run_subprocess(cmd, shell=None):
    """Run the given command in a subprocess."""
    if DRYRUN:
        telluser(cmd)
    else:
        log.info(cmd)
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

    sshcmd = '{} "{}" &'.format(CONFD["terminal_command"], build_sshcmd())
    log.info(sshcmd)
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
    telluser(s)


def handle_start(args):
    """Perform cmsd needed to start the docker and login

    I really need to monitor the success of the underlying
    cmds, instead of brute force sleep.
    [ ] {milestone} stop using sleep, monitor the subprocess for return values.
    """
    # do start up here
    cmds = build_dockerrun(args["latest"])
    for cmd in cmds:
        # TODO get better solution than sleep
        run_subprocess(cmd, shell=True)
        time.sleep(8)  # brute force give docker time to complete its stuff.
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
    cmd = "{} container ls".format(OCI_CMD)
    run_subprocess(cmd)
    cmd = "{} inspect run_devstation_next".format(OCI_CMD)
    txt = read_subprocess(cmd)
    jsond = json.loads(txt)
    ipaddress = jsond[0]['NetworkSettings']['IPAddress']
    print('Use this ip address {}'.format(ipaddress))


def handle_stop(args):
    """Kill the specified instance. """
    _latest = LATEST if args["latest"] else NEXT
    #: rewrite so this is not in two places
    instance_name = "run_{}_{}".format(CONFD["instance_name"], _latest)
    cmd = "{} container kill {}".format(OCI_CMD, instance_name)
    run_subprocess(cmd)


def hasValidConfig():
    """This is a placeholder for future development on checking curr env. """
    has_config_file = os.path.isfile(CONFIGLOCATION)
    return all([has_config_file])


def gatherinfo():
    questions = {
        "username": "What username should be the default (only) on your immutable workstation?"
    }
    answers = {}
    for label, question in questions.items():
        answer = input(question)
        answers[label] = answer
    return answers


def handle_quickstart(args):
    """We have a starter config on github. Pull that down and put in 
       users homedir, then alter based on questions.

    I am spending too long yak shaving on this app, and so will just
    print instructions and look to automate it later.
    """
    helpmsg = ""
    if hasValidConfig():
        helpmsg += """You appear to have an existing config in {}.
Please adjust it manually - view docs for help.""".format(
            CONFIGLOCATION
        )

    if not hasValidConfig():
        helpmsg += """ In the future this app will walk you through a series of
questions, but for now please can you download and unzip into {} the
starter config stored at {}.  You should have a directory layout like::

  .immutableworkstation
  |
  -config.ini
  |
  -.next/
  -.latest/

You should copy these into *your* github repo, and then update the 
templates to your needs, as you find a new package to be added to your 
workstation, adjust the config needed.

""".format(
            CONFIGDIR, STARTER_CONFIG_URL
        )

    telluser(helpmsg)


def handle_next2last(args):
    """ """
    # Note the extra dot
    _latestdir = "{}/.{}".format(CONFIGDIR, LATEST)
    _nextdir = "{}/.{}".format(CONFIGDIR, NEXT)
    _backupdir = "{}/latest.bak".format(CONFIGDIR)

    cmds = [
        "rm -rf {}".format(_backupdir),
        "mv -f {}  {}".format(_latestdir, _backupdir),
        "cp -r {} {}".format(_nextdir, _latestdir),
    ]
    input(
        "About to move {} and replace with {}. Hit any key".format(_latestdir, _nextdir)
    )
    for cmd in cmds:
        run_subprocess(cmd, shell=True)


def handle_unknown():
    telluser("Unknown request please type `devstation --help`")


def makeDocker(latest=True):
    """Take a .skeleton file, and replace defined markup with 
       contents of txt files

    Based on 'dockerfile.skeleton', replace any instance of 
    {{ python }} with the contents of file `templates\python.template`
    
    This is an *extremely* simple templating tool.  It is *not*
    supposed to have the complexity even of Jinja2.  Its supposed to 
    be really dumb.  Lucky I wrote it then :-).


    """

    _latest = "." + LATEST if latest else "." + NEXT
    current_folder = os.path.join(CONFD["devstation_config_root"], _latest)
    templates_folder = os.path.join(current_folder, "templates")
    pathtodockerfile = os.path.join(current_folder, "Dockerfile")
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
    """ aggregate print stmts into one place."""
    # handle my weird formatting
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
    elif args["next2last"]:
        handle_next2last(args)
    elif args["status"]:
        handle_status(args)
    elif args["stop"]:
        handle_stop(args)
    elif args["test"]:
        runtests()
    else:
        handle_unknown()


def runtests():
    import doctest

    doctest.testmod()


def main():
    global DRYRUN
    ## if we have not quickstart'd the config dir, only show quickstart option.
    if HASCONFIGDIR:
        args = docopt(DOCOPT_HELP)
    else:
        args = docopt(DOCOPT_HELP_SHORT)
    if args.get("--dryrun", False):
        DRYRUN = True
    run(args)


if __name__ == "__main__":
    main()
