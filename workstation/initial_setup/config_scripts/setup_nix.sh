#sudo apt install curl
sh <(curl -L https://nixos.org/nix/install) --daemon

Then we need to 
https://nix-community.github.io/home-manager/index.xhtml#sec-install-standalone

nix-channel --add https://github.com/nix-community/home-manager/archive/master.tar.gz home-manager

nix-channel --update

run this to setup 
nix-shell '<home-manager>' -A install

add this to ~/.profile
. "$HOME/.nix-profile/etc/profile.d/hm-session-vars.sh"
