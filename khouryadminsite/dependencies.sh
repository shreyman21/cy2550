#!/bin/bash

YELLOW='\033[0;33m'
GREEN='\033[0;32m'

# Update and upgrade the system
sudo apt-get update
sudo apt-get upgrade -y

# Install Python 3
sudo apt install python3 -y

# Install SQLite
sudo apt install sqlite3 -y

# Install Pip
sudo apt install python3-pip
sudo apt install python3-pip3

# Install Django using pip
# sudo apt install python3-pip -y
python3 -m pip3 install Django
pip3 install django

# Print installation status
echo -e "${YELLOW}All dependencies for this project have been installed successfully.${NC}"

# Verify the installation
python3 --version
sqlite3 --version
pip --version
pip3 --version
python3 -m django --version
