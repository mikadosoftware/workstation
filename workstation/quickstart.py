#! -*- coding:utf-8 -*-

"""
Very simple CLI based library that takes a dict of 'questions'
and asks them on CLI, and then returns answers.  THink of quick setup in 
sphinx docs

dict format is 

{'label': [<questiontext> , <defaultfunction>] 
...}
"""

import os

def run(questiond):
    """ """
    answerd = {}
    for label, data in questiond.items():
        questiontext = data[0]
        default_function = data[1]
        default_answer = default_function()
        answer = input(questiontext + " ['{}']: ".format(default_answer))
        if not answer:
            answer = default_answer
        answerd[label] = answer
        
    return answerd

def get_homedir():
    from os.path import expanduser
    home = expanduser("~")
    return os.path.join(home, ".devstation")

def example():
    d = {'devstationdir': ['Where to store config data?',
                            get_homedir]
         }
    print(run(d))
    # returns {'devstationdir': '/root/.devstation'}

if __name__ == '__main__':
    example()
