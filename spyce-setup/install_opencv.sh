#!/bin/bash

#Update and Upgrade
sudo apt update -y
sudo apt upgrade -y

echo "###################################################################################################"
echo "Updated and Upgraded. Expanding SWAPSIZE to 2048 MB"
echo "###################################################################################################"

spyce-setup/set_SWAPSIZE.sh 2048

echo "###################################################################################################"
echo "SWAPSIZE expanded to 2048 MB. Preparing to install dependecies"
echo "###################################################################################################"

#Install necessary packages for OpenCV
sudo apt install build-essential cmake pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libatlas-base-dev gfortran libhdf5-dev libhdf5-serial-dev libhdf5-103 libqt5gui5 libqt5webkit5 libqt5test5 python3-pyqt5 python3-dev libcanberra-gtk-module libcanberra-gtk3-module libopenblas-dev screen -y
pip3 install -U numpy
pip3 install -U pyserial
pip3 install adafruit-circuitpython-sht31d

#echo "###################################################################################################"
#echo "All dependencies installed. Preparing to download opencv."
#echo "###################################################################################################"

pip3 install opencv-contrib-python==4.5.3.56

# Check if OpenCV is installed in Python
if python -c "import cv2"; then
    echo "OpenCV is installed in Python! We're good to go."
else
    echo "OpenCV is not installed in Python :("
    echo "Try to import OpenCV in Python3 and see errors for any uninstalled dependencies."
fi