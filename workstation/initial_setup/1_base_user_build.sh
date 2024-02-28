#how to build a base
#-------------------
#I want a (fairly) stable workstation.
#Development environment - python venvs, in a docker, using ssh/terminal access
#user env - firefox, stable updates 
#migrate towards nix 
# write the book, get a draft for two of them. print out by end of next week.



# base user - getting podman etc ready
# dropbox etc for use
# develop in docker but need email etc - perhasp outdside? is this still a workstation

#We shall call all (idempotent) bash scripts in
#config_scripts, and each can assume they can use
#the following values.  
#THey should also assume they can add a 
#text value to manually run after instructions
#POST_RUN_INSTRUCTIONS+="Some notes"

#########################################################

SCRIPT_ROOT_DIR=`pwd`
USERNAME="pbrian"
USER_FULL_NAME="Paul Brian"
USER_EMAIL="paul@mikadosoftware.com"
USER_HOME_DIR="/home/$USERNAME"
POST_RUN_INSTRUCTIONS=''

#########################################################

files=()
search_dir=`pwd`/config_scripts

for entry in "$search_dir"/*
do
	files+=("$entry")
done

for i in "${files[@]}"
do
	echo "-------------------------"
	cat "$i"
	echo "--------------------------"
	read -p "Y?" executethis
	if [[ "$executethis" == "Y" ]]
	then
		echo "running"
		source $i
	fi

done


