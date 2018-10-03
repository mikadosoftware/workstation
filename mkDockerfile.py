#! -*- coding:utf-8 -*-

"""Dirt simple script to manage large Dockerfile(s)

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


compare
  Its useful to compare my original dockerfile with the generated one to see what I broke

"""
import os
import docopt

help = '''mkDockerfile

Usage:
    mkDockerfile.py
    mkDockerfile.py compare <LHS> <RHS>

Options:
    -h --help SHow this page

'''

def makeDocker():
    
    folder = 'templates'
    skeleton = 'dockerfile.skeleton'

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
    fo = open('Dockerfile', 'w')
    fo.write(outputs)
    fo.close()

def comparefiles(LHS, RHS):
    """line by line cmparisons """
    LHSlines = set([l.strip() for l in open(LHS).read().split("\n")])
    RHSlines = set([l.strip() for l in open(RHS).read().split("\n")])
    print("In {} not in {}".format(LHS, RHS))
    for line in LHSlines - RHSlines:
        print(line)
    print("\n\nIn {} not in {}".format(RHS, LHS))
    for line in RHSlines - LHSlines:
        print(line)
    
if __name__ == '__main__':
    args = docopt.docopt(help)
    if args['compare']:
        LHS = args['<LHS>']
        RHS = args['<RHS>']
        comparefiles(LHS, RHS)
    else:
        makeDocker()
    
