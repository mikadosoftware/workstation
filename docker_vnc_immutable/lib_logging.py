#!/usr/bin/python3
#! -*- coding:utf-8 -*-

"""
lib_logging
===========
    
"""
##### imports #####
import logging, sys

##### Module setup #####
# TODO: split out logging into common module
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
log.addHandler(handler)

