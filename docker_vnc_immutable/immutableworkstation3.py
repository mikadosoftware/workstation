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

usage
-----

We expect to have a config .ini file.  This is for ease of specifying things like
volume mappings.

By default the config file is at `~/immuntableworkstation/config.ini`

[ ] Implement expect-style testing so we can automate testing.
[x] put the home dir into git seperate to rest of pacakge (ie thats the indivudal part)
[ ] put blog.mikadosoftware onto AWS and run this testing with docker on it.
[ ] migrate rest of the articles there.
[x] create a plain docker instance and just import devstation, see if it works (ie clean install)
[ ] run the get github projects into one place 

[ ] podman system prune : clean up a lot of cruft in docker areas.
[x] remove priviledged access with auser name remapping
[ ] improve using https://github.com/mviereck/x11docker

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
import lib_config
import operator

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
    immutableworkstation.py showconfig [options]
    immutableworkstation.py createDockerfile --templatedir=<path> [options]
    immutableworkstation.py start tagname [options] 
    immutableworkstation.py stop tagname [options] 
    immutableworkstation.py login tagname [options]
    immutableworkstation.py buildAnyDocker <path_to_dockerfile> <context_dir> [options]
    immutableworkstation.py status
    immutableworkstation.py test
    immutableworkstation.py (-h | --help )


Options:
    -h --help                   Show this screen
    -d --dryrun                 dryrun
    --configfile=<configpath>   path 2 config ini file
    --tagname=<tagname>         Name to tag 
    --instancename=<instancename>
    --username=<username>
    --volumearray=<volumearray>


"""

def parse_docopt(argsd):
    '''We want to split into args (<val>), options (--left) and commands (foo.py fire) '''
    args = []
    options = []
    commands = []
    active_commmands = []
    # we assume only one command at a time?
    for k,i in argsd.items():
        if k.startswith("--"):
            options.append({k:i})
        elif k.startswith("<"):
            args.append({k:i})
        else:
            commands.append({k:i})
    # 
    active_commands = [list(d.keys())[0] for d in commands if list(d.values())[0]]
    return args, options, commands, active_commands      

############### Config
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
        --privileged \
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
    tmpl = "{} build -t {{tagname}}:{{tagtag}} {{pathtodockerfile}} --squash".format(OCI_CMD)
    _latest = LATEST if latest else NEXT
    pathtodockerfile = os.path.join(CONFD["devstation_config_root"], "." + _latest)
    return tmpl.format(
        tagname=CONFD["tagname"], tagtag=_latest, pathtodockerfile=pathtodockerfile
    )

def build_docker_any_build(path_to_dockerfile, context_dir):
    """Create command used to (re)build the container.

    """
    tmpl = "{} build -t {{tagname}}:{{tagtag}} -f {{path_to_dockerfile}} {{context_dir}}  --squash".format(OCI_CMD)
    return tmpl.format(
        tagname='anybuild', tagtag='0.1', path_to_dockerfile=path_to_dockerfile, context_dir=context_dir
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


############### Config
# This is a 'well-known' location
CONFIGDIR = os.path.join(os.path.expanduser("~"), ".immutableworkstation")
CONFIGLOCATION = os.path.join(
    os.path.expanduser("~"), ".immutableworkstation/config.ini"
)
def handle_showconfig(args):
    print(args['--configfile'])
    #lib_config.show_config(confd=CONFD)

def handle_login(args):
    spawn_sibling_console()

def handle_createDockerfile(args):
    makeDocker(args['--templatedir'])

def handle_buildDocker(args):
    """Trigger the processes to create new dockerfile and then build image. """
    makeDocker(latest=args["latest"])
    cmd = build_docker_build(latest=args["latest"])
    run_subprocess(cmd)

def parse_volumearray(args):
    ''' COnvert volumne array to usable instructions
    
    >>> parse_volumearray(args)
    '''
    x = ['~/data=/var/data', 
    '~/projects=/var/projects',
    '~/secrets=/var/secrets:ro',
    '~/Dropbox=/var/Dropbox']
    return x 

def handle_buildAnyDocker(args):
    """Trigger the processes to create new dockerfile and then build image. """
    #import pdb;pdb.set_trace()
    cmd = build_docker_any_build(args['<path_to_dockerfile>'], args['<context_dir>'])
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

def handle_unknown(command, e, args):
    telluser(f"Unknown request.  We got command: {command} and error: {e}.  Full args were {args}")


def makeDocker(templatesdir):
    """Take a .skeleton file, and replace defined markup with 
       contents of txt files

    Based on 'dockerfile.skeleton', replace any instance of 
    {{ python }} with the contents of file `templates\python.template`
    
    This is an *extremely* simple templating tool.  It is *not*
    supposed to have the complexity even of Jinja2.  Its supposed to 
    be really dumb.  Lucky I wrote it then :-).


    """
    pathtodockerfile = os.path.join(templatesdir, "../Dockerfile")
    skeleton = "dockerfile.skeleton"
    outputs = ""
    with open(os.path.join(templatesdir, skeleton)) as fo:
        for line in fo:
            if line.find("{{") == 0:
                file = line.replace("{{", "").replace("}}", "").strip()
                filepath = os.path.join(templatesdir, file + ".template")
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

def build_current_confd(args, options, commands, active_commands):
    print("args", args, '----\n')
    print("options", options, '----\n')
    print("commands", commands, '----\n')
    print("active commands", active_commands, '----\n')
    volumes = parse_volumearray(options)
    import sys; sys.exit()
    
def run(argsd):
    #: start with quickstart as it may be our only options
    #: [ ] make this safer with .get
    args, options, commands, active_commands = parse_docopt(argsd)
    build_current_confd(args, options, commands, active_commands)
    for active_command in active_commands:
        try:
            # in current module, prepend handle_ to the name of the active command and
            # look for that in current module, if it exists, call it
            current_module = sys.modules[__name__] 
            fn = operator.attrgetter('handle_{}'.format(active_command))(current_module)
            fn.__call__(argsd)
        except Exception as e:
            handle_unknown(active_command, e, argsd)

def runtests():
    import doctest
    doctest.testmod()

teststr = '''
[default]
tagname   = workstation
instance_name = devstation
localhost  = 127.0.0.1
username   = pbrian
ssh_port   = 2222
terminal_command = /usr/bin/konsole -e
volume_array: ~/secrets=/var/secrets:ro ~/secrets2=/var/secrets2:ro 

'''
def main():
    global DRYRUN
    args = docopt(DOCOPT_HELP)
    if args.get("--dryrun", False):
        DRYRUN = True
    run(args)


if __name__ == "__main__":
    main()
