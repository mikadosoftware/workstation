# 1. package installation

sudo apt update -y && sudo apt upgrade -y

targetpkgs=(build-essential
            libssl-dev 
            libffi-dev 
            python3-dev
            python3-pip
            python3-venv 
            podman
    )
            
for pkg in ${targetpkgs[@]}
do
    sudo apt install $pkg -y
done


