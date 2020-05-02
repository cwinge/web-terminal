#!/bin/bash

# need to run everything as sudo, at least on GCS

# update repos
sudo apt update

# install docker & make it functioning
sudo apt install -y docker.io
sudo usermod -aG docker ${USER}
sudo systemctl start docker
sudo systemctl enable docker
sudo systemctl restart docker
# Fix for daemon issue that sometimes present itself...
sudo chmod 666 /var/run/docker.sock 

# install python3
sudo apt install -y python3

# install pip3
sudo apt install -y python3-pip

# install python modules
pip3 install flask
pip3 install wtforms

# install GoTTY
wget https://github.com/yudai/gotty/releases/download/v2.0.0-alpha.3/gotty_2.0.0-alpha.3_linux_amd64.tar.gz
tar xvf gotty_2.0.0-alpha.3_linux_amd64.tar.gz
chmod +x gotty
sudo mv gotty /usr/local/bin/
rm gotty_2.0.0-alpha.3_linux_amd64.tar.gz

#install tmux
sudo apt install -y tmux

#install jq - used to get docker container size via docker API
sudo apt install -y jq

# clone git repo
git clone https://github.com/cwinge/web-terminal

# create custom docker container, takes a while... can omit and run at a later time
cd web-terminal
docker build -t customenv .

# run the server with the following commands
# tmux
# python3 main.py <insert external ip>
# e.g. python3 main.py 0.0.0.0
