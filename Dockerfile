FROM ubuntu:18.04
MAINTAINER pbrian
LABEL Name="pbriandev" Version=0.0.1

### Constants
ENV WKDIR /staging
ENV USERHOME /home/pbrian

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
                       wget \
                       x11-apps

###### symlinking to have `pip` and `python`
RUN cd /usr/bin \
       && ln -sf python3.6 python \
       && ln -sf python3.6 python3

############ Install pip (bootstrapping)
# if this is called "PIP_VERSION", pip explodes with "ValueError: invalid truth value '<VERSION>'"
# 18.04 does not have it but get-pip expects it
RUN apt-get install -y python3-distutils python3-distlib 

ENV PYTHON_PIP_VERSION 10.0.1

RUN set -ex; \
	\
	wget -O get-pip.py 'https://bootstrap.pypa.io/get-pip.py'; \
	\
	python get-pip.py \
		--disable-pip-version-check \
		--no-cache-dir \
		"pip==$PYTHON_PIP_VERSION" \
	; \
	pip --version; \
	\
	find /usr/local -depth \
		\( \
			\( -type d -a \( -name test -o -name tests \) \) \
			-o \
			\( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
		\) -exec rm -rf '{}' +; \
	rm -f get-pip.py

#####

### update python pkgs
# Install any needed packages (ie above those for the runtime)
RUN pip install --trusted-host pypi.python.org sphinx \
                                               pytest \
					       pylint

### end python

### Create SSH access to box
### NB Fix root access 
RUN mkdir -p /var/run/sshd		       
RUN echo 'root:root' | chpasswd	
RUN sed -ri 's/^#PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config
RUN sed -ri 's/^#AllowTcpForwarding\s+.*/AllowTcpForwarding yes/g' /etc/ssh/sshd_config
RUN sed -ri 's/^#X11Forwarding\s+.*/X11Forwarding yes/g' /etc/ssh/sshd_config
RUN sed -ri 's/^#X11UseLocalhost\s+.*/X11UseLocalhost no/g' /etc/ssh/sshd_config


#################### Misc config ##########################
## Locales
# TBD

## fonts
RUN apt-get -y install fonts-inconsolata

### HOME 
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
 
EXPOSE 22
ENTRYPOINT ["/home/pbrian/ENTRYPOINT.sh"]
#CMD ["/usr/sbin/sshd", "-D"]
