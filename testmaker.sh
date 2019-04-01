# This plus the assoc Dockerfile just gives me a repeatable 
# clean ubunut instance so I can repeatebly develop the setup code 

echo "Run the below after getting a container shell, which will start next" 
TGT=~/projects/installworkstation.sh
echo pip3 install /var/projects/workstation/dist/workstation-0.0.1-py3-none-any.whl > $TGT
echo pip3 install /var/projects/MikadoLib/dist/mikadolib-0.0.1-py3-none-any.whl >> $TGT
echo pip3 install /var/projects/workstation/docopt-0.6.2.tar.gz >> $TGT

## use this to build a container 
## sudo docker build -t tag_tester .
sudo docker run -i -v /home/pbrian/projects:/var/projects -t tag_tester:latest
