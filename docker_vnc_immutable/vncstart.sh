
catch_err() {
    echo "An error occured. Commonly this needs a podman container prune to remove container image with same name."
}

trap 'catch_err' ERR
# remove any stopped, old versions of the container that prevent rerunning
# best to provide new name
podman container prune
podman run --rm                    \
  --interactive                    \
  --tty                            \
  --volume /run/user/$(id -u)/pulse/native:/run/user/1000/pulse/native \
  --volume /home/pbrian/data:/var/data:z \
  --volume /home/pbrian/projects:/var/projects  \
  --volume /home/pbrian/secrets:/var/secrets:ro  \
  --volume /home/pbrian/Dropbox:/var/Dropbox  \
  --userns=keep-id \
  --publish ${VNC_PORT:-5900}:5900 \
  --name immutableworkstation      \
  --env LANG=en_GB.UTF-8           \
  --env DESKTOP_SIZE="1920x1000"   \
  --env DESKTOP_BACKGROUND_IMAGE="https://apod.nasa.gov/apod/image/2210/JovianEclipse1024c.jpg" \
  --detach \
  mikado-immutableworkstation

sleep 15
vncviewer localhost:0

# test out sounds with
## paplay /usr/share/sounds/freedesktop/stereo/bell.oga
## you should hear a sound on PC speaker and hey presto, desktop.
## As a confirmed tone-deaf music-o-philistine please do not ask for anything clever in the audio world

