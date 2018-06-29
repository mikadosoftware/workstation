#Kill existing docker
sudo docker container kill run_wkstn
sh build/build.sh 
sh build/run.sh
sleep 10
sh build/login.sh

