#! -*- coding:utf-8 -*-

from setuptools import setup, find_packages
import glob
import os

import sys
from pprint import pprint as pp

def get_data_files(inrepo_dirlist):
    """Python Packaging is (still) awkward.  I am writing this longform as
    it took a long time to work out and there are no good answers
    online as yet.

    In some cases I want to include non-python files in my wheel /
    distribution.  This might be obvious stuff like License files or
    in workstation cases, config files just to be added to allow
    configuration of the bin script.

    Python distutils/setuptools has concepts of both `data_files` and
    `package_data`.  `package_data` is non-python files stored inside
    the python package (i.e. the parts marked by `__init__.py`
    directories).  The aim is to *distribute* those onto target disk
    inside the pacakge directories again.

    `data_files` are kept outside of pacakge directories, in the repo
    as well as on target disk.  `data_files` should be written to
    target disk at `sys.prefix()`, but it seems that has changed in
    code and is now landing at '/usr/local'.
    
    the data_files parameter in setup expects a list of tuples like::

        ('config/.next/templates', ['config/.next/templates/apt.template'])
 
    Each tuple represents one file to be distributed, globbing is not
    working so well.  the left hand side is the format of directory
    structure to be created on target disk under /usr/local and the
    right hand is the path of the file *in the repo* that will be
    placed on target disk.

    This is correct for `setuptools.__version__ == '39.0.1'`

    So now we build a helper to get and then retireve the data files
    just so I can populate them in the users local dir

    [X] list dirs to search / rebuild
    [ ] recovery - how to find where we put them?? !!

    """
    
    data_files = []
    for folder in inrepo_dirlist:
        for dirpath, dirnames, filenames in os.walk(folder):
            data_files.append((dirpath, [os.path.join(dirpath, f) for f in filenames]))
            
    return data_files

import shutil
def _copy_my_files():
    os.mkdir('/home/pbrian/.devstation')
    shutil.copytree('/usr/local/config/', '/home/pbrian/.devstation')
    
# get version data
with open("VERSION") as fo:
    version = fo.read()

setup(
     name='workstation',
     version=version,
     description='An approach to Immutable Workstations on various hosts',
     author='See AUTHORS.txt',
     packages=find_packages(exclude=('tests')),

    ## for some godforsaken reaosn these are put into /usr/local
    ## (close but off accoridng to docs https://docs.python.org/2/distutils/setupscript.html#installing-package-data

    # files outside the package ...?
    
#    data_files=get_data_files(['config/',]),
    #files inside the pacakge ???
#    package_data={'workstation': ['LICENSE', 'AUTHORS', 'config/*']},
#    include_package_data=True,
    # Any scripts (i.e. python/bash) here will be added to PATH (/usr/local/bin)
    scripts=glob.glob('bin/*'),



    install_requires=[
        "mikado-core"
    ]
)
