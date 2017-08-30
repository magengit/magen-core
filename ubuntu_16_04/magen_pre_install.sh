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

sudo add-apt-repository -y ppa:jonathonf/python-3.6
sudo apt-get -qq update
sudo apt-get -y install python3.6
sudo apt-get -y install python3.6-dev

sudo apt-get -y install python3-pip
sudo -H pip3 install -U pip setuptools

#echo "alias python=python3" >> ~/.bashrc

sudo -H pip install --upgrade --user awscli
sudo -H apt-get install -y awscli

## Install Mongo
## https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
echo "deb [ arch=amd64,arm64 ] http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
sudo apt-get update
sudo apt-get -y install -y mongodb-org
sudo chown -R mongodb:mongodb /var/lib/mongodb
# Allowing connections to other interfaces besides loopback
sudo sed -i.bak '/bindIp/d' /etc/mongod.conf
sudo service mongod start

## In order to run Docker automation you need to install Docker as descried here.
## https://docs.docker.com/engine/installation/linux/ubuntulinux/

sudo apt-get -y install apt-transport-https ca-certificates
sudo apt-key adv \
               --keyserver hkp://ha.pool.sks-keyservers.net:80 \
               --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
echo "deb https://apt.dockerproject.org/repo ubuntu-xenial main" | sudo tee /etc/apt/sources.list.d/docker.list
sudo apt-get -qq update
sudo apt-get -y install linux-image-extra-$(uname -r) linux-image-extra-virtual
apt-cache policy docker-engine
sudo apt-get -y --allow-unauthenticated install docker-engine
sudo service docker start
sudo docker run hello-world


sudo curl -o /usr/local/bin/docker-compose -L "https://github.com/docker/compose/releases/download/1.11.2/docker-compose-$(uname -s)-$(uname -m)"
sudo chmod +x /usr/local/bin/docker-compose
docker-compose -v

## upload code with Pycharm  important
## sudo –H make clean
## make package
## sudo –H make install
