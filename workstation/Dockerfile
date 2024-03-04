# From skelton
FROM    ubuntu:jammy
LABEL   maintainer="cyd@9bis.com"

#ARG     PROXY_CERT 
#RUN     test -z "${PROXY_CERT}" || { echo "${PROXY_CERT}" | base64 -d | tee /usr/local/share/ca-certificates/ca-local.crt > /dev/null && update-ca-certificates ; }

# We prepare environment
ARG     TZ=${TZ:-Etc/UTC}
ARG     DEBIAN_FRONTEND=noninteractive
RUN     \
        echo "Timezone and locale" >&2                     \
        && apt-get update                                  \
        && apt-get install -y                              \
          apt-utils                                        \
          software-properties-common                       \
          tzdata sudo                                          \
        && apt-get clean                                   \
        && apt-get autoremove -y                           \
        && rm -rf /tmp/* /var/tmp/*                        \
        && rm -rf /var/lib/apt/lists/* /var/cache/apt/*    \
        && echo "Timezone and locale OK" >&2






# We add a simple user with sudo rights
ENV     USERNAME=pbrian
ENV     USERHOME=/home/pbrian
ARG     USR_UID=1000
ARG     USR_GID=5000

RUN     groupadd --gid ${USR_GID} ${USERNAME}                                       
RUN     useradd --uid ${USR_UID} --create-home --gid ${USR_GID} --shell /bin/bash ${USERNAME}
RUN     echo "${USERNAME}:${USERNAME}" | chpasswd                     
RUN     echo ${USERNAME}'     ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers 


RUN echo 'root:root' | chpasswd
### Setup me as only user .... because I will be !
# RUN useradd -m -c "$USERFULLNAME" $USERNAME --shell /bin/bash 
# RUN usermod -aG sudo $USERNAME
# RUN echo "$USERNAME:$USERNAME" | chpasswd

# change user locale settings (see baseconfig)
RUN echo "export LC_ALL=en_GB.UTF-8" >> $USERHOME/.bashrc
RUN echo "export LC_LANGUAGE=en_GB.UTF-8" >> $USERHOME/.bashrc

# This is really just the config settings 
# any secrfets are added via '/var/secrets' volume per run
# as such this is a "safe" image to keep on say a hub
# COPY rcassets/.emacs $USERHOME
# COPY rcassets/.pylintrc $USERHOME
#COPY rcassets/.gitconfig $USERHOME
#COPY rcassets/.ssh $USERHOME/.ssh
#RUN chown -R $USERNAME:$USERNAME $USERHOME/.ssh
#RUN chown -R $USERNAME:$USERNAME $USERHOME/.gitconfig
#

### {{ apt }}

# build the basic development world
RUN apt-get update && \
    apt-get install -y apt-transport-https \
                       build-essential \
                       dos2unix \
                       git \
                       openssh-server \
                       wget curl \
                       && \
	apt-get clean

# We add some tools
RUN     \
        echo "Install some tools" >&2                      \
        && apt-get update                                  \
        && apt-get install -y --no-install-recommends      \
          curl                                             \
          dumb-init                                        \
          jq                                               \
          libnss3-tools                                    \
          mlocate                                          \
          net-tools                                        \
          xz-utils                                         \
          zip                                              \
        && apt-get install -y thunar-archive-plugin        \
        && apt-get clean                                   \
        && apt-get autoremove -y                           \
        && rm -rf /tmp/* /var/tmp/*                        \
        && rm -rf /var/lib/apt/lists/* /var/cache/apt/*    \
        && echo "Install some tools OK" >&2

### {{ baseconfig }}

#################### Misc config ##########################
## Locales
# We dont have any languages setup at this point
# 
RUN apt-get update && \
    apt-get install -y locales && \
    locale-gen en_GB.UTF-8 && \
    update-locale LC_ALL=en_GB.UTF-8 LANGUAGE=en_GB.UTF-8 && \
    apt-get clean
    
#these need to be run in user sections
#RUN echo "export LC_ALL=en_GB.UTF-8" >> /home/pbrian/.bashrc
#RUN echo "export LC_LANGUAGE=en_GB.UTF-8" >> /home/pbrian/.bashrc

#THis should now work in our terminal (prints Greek for Thank you)
#python3 -c "print(u''.join([u'\u0395', u'\u03c5', u'\u03c7', u'\u03B1', u'\u03c1', u'\u03B9', u'\u03C3', u'\u03c4', u'\u03c9']))"

## fonts
RUN apt-get -y install fonts-inconsolata && apt-get clean

ENV TZ=Europe/London
ENV DEBIAN_FRONTEND=noninteractive
RUN DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y tzdata \
    && apt-get clean
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone



### {{ otherdevtools }}


### Other Dev Tools
RUN apt-get install -y	whois 




### {{ github_cli }}

# from cli github page:
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
&& chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
&& apt update \
&& apt install gh -y \
&& apt-get clean

RUN echo "READY TO DO PYTHON"
###### Install with apt
RUN apt-get install -y libpython3.10 \
                       python3.10 \
                       python3-pip \
		       && apt-get clean

###### symlinking to have `pip` and `python`
RUN cd /usr/bin \
       && ln -sf python3.10 python \
       && ln -sf python3.10 python3 \
       && ln -sf pip3 pip

#####
RUN python3 -m pip install --upgrade pip
#RUN python3 -m pip install pygithub

### update python pkgs
# Install any needed packages (ie above those for the runtime)
RUN pip install --trusted-host pypi.python.org sphinx \
                                               pytest \
					       pylint


#RUN pip install -r $WKDIR/requirements.txt
RUN pip install -r $WKDIR/unpinned_requirements.txt
# Additonal setup for spacy.  I think this is sensible to do specify in this file them
#RUN python -m spacy download en
RUN echo "READY TO DO PYTHON END"
# seems ubunut installs pip_internal again mucking things up

# lastly redo symlinks
RUN rm /usr/bin/python
RUN ln -s /usr/bin/python3 /usr/bin/python





# We add sound
# add root user to group for pulseaudio access
RUN adduser root pulse-access
RUN     printf 'default-server = unix:/run/user/1000/pulse/native\nautospawn = no\ndaemon-binary = /bin/true\nenable-shm = false' > /etc/pulse/client.conf


# We set localtime
RUN      if [ "X${TZ}" != "X" ] ; then if [ -f /usr/share/zoneinfo/${TZ} ] ; then rm -f /etc/localtime ; ln -s /usr/share/zoneinfo/${TZ} /etc/localtime ; fi ; fi

# And here is the statup script, everything else is in there
COPY    entrypoint.sh /entrypoint.sh
RUN     chmod 755 /entrypoint.sh

# We do some specials
RUN     \
        updatedb ;                                       \
        apt-get clean                                    \
        && apt-get autoremove -y                         \
        && rm -rf /tmp/* /var/tmp/*                      \
        && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

# We change user
USER    ${USERNAME}
WORKDIR /home/${USERNAME}
COPY    functions.sh /home/${USERNAME}/.functions.sh
COPY    bgimage.jpg /usr/share/backgrounds/xfce/bgimage.jpg
RUN     \
        printf 'if [[ $- = *i* ]] ; then test -f ~/.functions.sh && . ~/.functions.sh ; fi' >> /home/${USERNAME}/.bashrc

#ENTRYPOINT [ "/usr/bin/dumb-init", "--", "/entrypoint.sh" ]
ENTRYPOINT [ "/entrypoint.sh" ]
