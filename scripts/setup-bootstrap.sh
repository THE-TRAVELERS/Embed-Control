#!/bin/bash

# Install the alias file
echo "----- Installing the alias config -----"

curl -O https://raw.githubusercontent.com/THE-TRAVELERS/Embed-Control/main/scripts/.bash_aliases
mv .bash_aliases ~/.bash_aliases

echo "----- Finished installing the alias config -----\n"


# Install the rc.local file for running the hotspot on boot
echo " ----- Installing the hotspot config -----"

curl -O https://raw.githubusercontent.com/THE-TRAVELERS/Embed-Control/main/scripts/rc.local
sudo mv rc.local /etc/rc.local

echo "----- Finished installing the hotspot config -----\n"

# Setting up src files
echo "----- Setting up the src files -----"

cd ~/Documents
mkdir Projects
mkdir Env
cd Projects
git clone https://github.com/THE-TRAVELERS/Embed-Control.git

echo "----- Finished setting up the src files -----\n"

# Setting up the virtual environment
echo "----- Setting up the virtual environment -----"

sudo apt install libcap-dev
cd ~/Documents/Env
python3 -m venv -m venv --system-site-packages api_env
source api_env/bin/activate
cd ~/Documents/Projects/Embed-Control/src/command/Rpi/
pip install -r requirements.txt

echo "----- Finished setting up the virtual environment -----\n"

# Setting up the service
echo "----- Setting up the service -----"

cd ~
curl -O https://raw.githubusercontent.com/THE-TRAVELERS/Embed-Control/main/scripts/api.service
sudo mv api.service /etc/systemd/system/api.service
sudo systemctl enable api.service
sudo systemctl start api.service

echo "----- Finished setting up the service -----\n"

# Rebooting the system
echo "----- Rebooting the system in 10s -----"

sleep 10
sudo reboot
