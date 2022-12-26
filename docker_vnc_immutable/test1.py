
#my application

# env :
# export SETTINGS_FILE_FOR_DYNACONF='["/home/pbrian/.immutableworkstation/settings.ini",]'


import os
#print(os.environ)
for i in os.environ.keys():
    if i.startswith('DYNACONF'):
        print(i, os.environ[i])

from lib_config import settings
#dynaconf_include = ["/home/pbrian/foo.ini"]
print(settings.values())