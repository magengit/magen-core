#!/usr/bin/env bash

# This script helps bring up the environment on Ubuntu 16.04 for Magen services

#sudo apt-get update
sudo apt-get -qq update
sudo apt-get install -y apt-utils
sudo apt-get install -y wget
sudo apt-get install -y xz-utils
sudo apt-get install -y build-essential
sudo apt-get install -y libsqlite3-dev
sudo apt-get install -y libreadline-dev
sudo apt-get install -y libssl-dev
sudo apt-get install -y libffi-dev
sudo apt-get install -y openssl
sudo apt-get install -y net-tools
sudo apt-get install -y apt-transport-https
sudo apt-get install -y ca-certificates
sudo apt-get install -y curl
sudo apt-get install -y software-properties-common

sudo add-apt-repository -y ppa:jonathonf/python-3.6
sudo apt-get -qq update
sudo apt-get -y install python3.6
sudo apt-get -y install python3.6-dev

sudo apt-get -y install python3-pip
sudo pip3 install --upgrade pip setuptools

sudo -H pip install --upgrade --user awscli
sudo -H apt-get install -y awscli

## Install Mongo
## https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.6 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.6.list
sudo apt-get update
sudo apt-get -y install -y mongodb-org
#sudo chown -R mongodb:mongodb /var/lib/mongodb
# Allowing connections to other interfaces besides loopback

#FILE="/etc/systemd/system/mongodb.service"
#/bin/cat <<EOM >$FILE
#[Unit]
#Description=High-performance, schema-free document-oriented database
#After=network.target
#
#[Service]
#User=mongodb
#ExecStart=/usr/bin/mongod --quiet --config /etc/mongod.conf
#
#[Install]
#WantedBy=multi-user.target
#EOM

#sudo service mongod start
#sudo service mongod status

#sudo systemctl start mongodb
#sudo systemctl enable mongodb
#sudo systemctl status mongodb
mongo --eval 'db.adminCommand( { setFeatureCompatibilityVersion: "3.4" } )'
mongo --eval 'db.adminCommand( { getParameter: 1, featureCompatibilityVersion: 1 } )'


## In order to run Docker automation you need to install Docker as described here.
## https://docs.docker.com/engine/installation/linux/ubuntulinux/

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get update
sudo apt-get install -y docker-ce
sudo groupadd docker
sudo usermod -aG docker $USER
docker run hello-world
sudo systemctl enable docker

## Docker compose

sudo curl -L https://github.com/docker/compose/releases/download/1.17.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version

# Set Python default

#echo "alias python3=python3.6" >> ~/.bashrc
echo "alias python=python3.6" >> ~/.bashrc

sudo update-alternatives --install /usr/bin/python3 python /usr/bin/python3.6 1
sudo update-alternatives --install /usr/bin/python3 python /usr/bin/python3.5 2
sudo update-alternatives --list python
sudo update-alternatives --set python /usr/bin/python3.6

curl -o get-pip.py https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
# sudo pip3 install --upgrade pip setuptools

# REBOOT

sudo reboot


## upload code with Pycharm  important
## sudo –H make clean
## make package
## sudo –H make install
