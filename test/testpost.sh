# This plus the assoc Dockerfile just gives me a repeatable 
# clean ubunut instance so I can repeatebly develop the setup code 

#echo "Run the below after getting a container shell, which will start next" 
pip3 install /var/projects/workstation/dist/workstation-0.0.1-py3-none-any.whl
pip3 install /var/projects/workstation/docopt-0.6.2.tar.gz
pip3 install /var/projects/mikado-core/dist/mikado_core-0.0.3-py3-none-any.whl

