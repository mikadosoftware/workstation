#!/usr/bin/python3
#! -*- coding:utf-8 -*-

"""
lib_config
==========

A library file for doing config-related things

usage
-----

We expect to have a config .ini file.  This is for ease of specifying things like
volume mappings.

By default the config file is at `~/immuntableworkstation/config.ini`


An example
-----------

::

    [default]
    tagname   = workstation
    instance_name = devstation
    localhost  = 127.0.0.1
    username   = pbrian
    ssh_port   = 2222
    terminal_command = /usr/bin/konsole -e
    [volumes]
    ~/data=/var/data
    ~/projects=/var/projects
    ~/secrets=/var/secrets:ro
    ~/Dropbox=/var/Dropbox
    ~/.immutableworkstation=/var/.immutableworkstation
    volume_1=~/data=/var/data
    
"""
##### imports #####
import logging

######### THird party library for config mgmt #################
from dynaconf import Dynaconf

from dynaconf import LazySettings

# cannot use ~ ???
settings = LazySettings(
  PRELOAD_FOR_DYNACONF=["/home/pbrian/workstation_settings.ini",],    # <-- Loaded first
  SETTINGS_FILE_FOR_DYNACONF="/etc/immutableworkstation/settings.ini",          # <-- Loaded second (the main file)
  INCLUDES_FOR_DYNACONF=["other.module.settings", ]       # <-- Loaded at the end
)

# settings = Dynaconf(
#     envvar_prefix="DYNACONF",
#     settings_files=[ '.secrets.ini', '~/.env'],
# )

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
# '/home/pbrian/.immutableworkstation/settings.ini',
# export DYNACONF_SETTINGS=/home/pbrian/.immutableworkstation/settings.ini
###############################################################
