FROM ubuntu:18.04
MAINTAINER pbrian
LABEL Name="pbriandev" Version=0.0.1

### Constants
ENV WKDIR /staging
ENV USERHOME /home/pbrian
RUN mkdir $WKDIR

#Investigate this more
ENV DEBIAN_FRONTEND=noninteractive


### {{ apt }}

# build the basic development world
RUN apt-get update && \
    apt-get install -y apt-transport-https \
                       build-essential \
                       build-essential \
                       dbus-x11 \
                       dos2unix \
                       emacs25 \
                       fonts-inconsolata \
                       git \
                       konsole \
                       libpython3.6-dev \
                       openssh-server \
                       python3.6 \
                       python3.6-dev \
                       software-properties-common \
                       wget curl \
                       x11-apps \
                       firefox



### {{ baseconfig }}

#################### Misc config ##########################
## Locales
# TBD

## fonts
RUN apt-get -y install fonts-inconsolata




ENV TZ=Europe/London
#not ideal
ENV DEBIAN_FRONTEND=noninteractive
RUN DEBIAN_FRONTEND=noninteractive && apt-get install -y tzdata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone



### {{ otherdevtools }}


### Other Dev Tools
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get install -y nodejs
RUN npm install -g create-react-app
# this has to be done when instance is running ...
# RUN cd /var/projects/learnreact && create-react-app test1



### {{ sshX }}

### Create SSH access to box
### NB Fix root access 
RUN mkdir -p /var/run/sshd		       
RUN echo 'root:root' | chpasswd	
RUN sed -ri 's/^#PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config
RUN sed -ri 's/^#AllowTcpForwarding\s+.*/AllowTcpForwarding yes/g' /etc/ssh/sshd_config
RUN sed -ri 's/^#X11Forwarding\s+.*/X11Forwarding yes/g' /etc/ssh/sshd_config
RUN sed -ri 's/^#X11UseLocalhost\s+.*/X11UseLocalhost no/g' /etc/ssh/sshd_config





### {{ latex }}


### {{ user }}


### Setup me as only user .... because I will be !
RUN apt-get install sudo
RUN useradd -m -c 'Paul Brian' pbrian --shell /bin/bash 
RUN usermod -aG sudo pbrian
RUN echo 'pbrian:pbrian' | chpasswd

# This is really just the config settings 
# any secrfets are added via '/var/secrets' volume per run
# as such this is a "safe" image to keep on say a hub
COPY rcassets/.emacs $USERHOME
COPY rcassets/.pylintrc $USERHOME
COPY rcassets/.gitconfig $USERHOME
COPY rcassets/.ssh $USERHOME/.ssh
COPY rcassets/.emacs.d $USERHOME/.emacs.d
#
COPY rcassets/ENTRYPOINT.sh $USERHOME
COPY rcassets/ENTRYPOINT.sh $USERHOME
RUN chmod 0777 $USERHOME/ENTRYPOINT.sh




### {{ py3 }}

###### Install with apt
RUN apt-get update &&  apt-get install -y python3.6 \
                       python3.6-dev \
                       python3-distutils \
                       python3-distlib \
                       python3-pip

###### symlinking to have `pip` and `python`
RUN cd /usr/bin \
       && ln -sf python3.6 python \
       && ln -sf python3.6 python3 \
       && ln -sf pip3 pip

#####
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install pygithub

### update python pkgs
# Install any needed packages (ie above those for the runtime)
RUN pip install --trusted-host pypi.python.org sphinx \
                                               pytest \
					       pylint \
                                               black


# install requirements file. (why not specify in thisfile???)
COPY rcassets/requirements.txt $WKDIR/
RUN pip install -r $WKDIR/requirements.txt
# Additonal setup for spacy.  I think this is sensible to do specify in this file them
RUN python -m spacy download en

# seems ubunut installs pip_internal again mucking things up

# lastly redo symlinks
RUN rm /usr/bin/python
RUN ln -s /usr/bin/python3 /usr/bin/python


EXPOSE 22
ENTRYPOINT ["/home/pbrian/ENTRYPOINT.sh"]


