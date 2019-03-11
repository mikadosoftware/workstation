===========================================
Using Docker to test my application install
===========================================

I launched `immutable-workstation` as a bunch of shell files.
Which was *fine* except I wanted to make it eaasy to start using.

So I went yak shaving, and have written python command line tool, that will
run various workstation commands, most notably, it will do a intial quicksetup.

Well I hope it will, and that leads me to *testing* it.

Mostly this is a problem of first time setup. Luckily Docker excels at 
being a testbed for first time setup ! Hurrah.



Next - using github on command line to respond to issues etc


I am creating a linux docker that I will use to install and test the quicksetup feature 
of Docker. 

Dockerfile is kept short and simple ::

    FROM ubuntu:18.04
    MAINTAINER pbrian
    LABEL Name="pbriandev" Version=0.0.1

    ### Constants
    ENV WKDIR /staging
    ENV USERHOME /home/pbrian
    RUN mkdir $WKDIR
    ## {{ py3 }}

    ###### Install with apt
    RUN apt-get update && \
        apt-get install -y python3.7 \
                           python3.7-dev \
                           python3-distutils \
                           python3-distlib \
                           python3-pip


    CMD ["/bin/bash"]

sudo docker run -it tag_tester:latest
sudo docker build -t tag_tester .
