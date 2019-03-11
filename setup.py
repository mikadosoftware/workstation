#! -*- coding:utf-8 -*-

from setuptools import setup, find_packages
import glob


def get_data_files():
    """We have Python Packaging

    Ok - I want to include non python files in my wheel.
    SO these will be dropped off at sys.prefix (sortof) - /usr/local
    THen each of the tuples below will be taken from RIGHT tuple and
    added to left tuple prefixed by /usr/local 

    setuptools.__version__ == '39.0.1'
    SO now we build a helper to get and then retireve the data files
    just so I can populate them in the users local dir

    [ ] list dirs to search / rebuild
    [ ] recovery - just hardcode and grab !! 
    """
    return [('config', ['config/config.ini']),
            ('config/.next/templates', ['config/.next/templates/apt.template'])
           ]


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
    
    data_files=get_data_files(),
    #files inside the pacakge ???
#    package_data={'workstation': ['config/config.ini', 'LICENSE', 'AUTHORS']},
#    include_package_data=True,
    # Any scripts (i.e. python/bash) here will be added to PATH (/usr/local/bin)
    scripts=glob.glob('bin/*')
)
