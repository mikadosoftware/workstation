
sudo docker container prune -f
sudo docker run -d \
 -v ~/data:/var/data \
 -v ~/projects:/var/projects \
 -v ~/secrets:/var/secrets:ro \
 --name run_wkstn \
 -p 2222:22 \
 workstation:latest

