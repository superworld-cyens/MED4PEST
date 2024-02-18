#!/bin/bash

# Update and upgrade Raspberry Pi
echo "Updating and upgrading Raspberry Pi..."
sudo apt-get update
sudo apt-get upgrade -y

# Install Python virtual environment package
echo "Installing Python virtual environment package..."
sudo apt install python3-venv -y

# Create a Python virtual environment named .spy
echo "Creating Python virtual environment named .spy..."
python3 -m venv .spy

# Activate the virtual environment
echo "Activating the virtual environment..."
source .spy/bin/activate

# Install dependency packages
echo "Installing dependency packages..."
sudo apt-get install build-essential cmake git pkg-config libjpeg-dev libtiff5-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgtk2.0-dev pkg-config -y

# Install requirements from the provided requirements.txt file
echo "Installing Python packages from requirements.txt..."
pip install -r spyce-setup/requirements.txt

echo "Setup complete."
