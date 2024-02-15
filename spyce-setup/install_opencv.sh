#!/bin/bash

#Update and Upgrade
sudo apt update
sudo apt upgrade

echo "###################################################################################################"
echo "Updated and Upgraded. Expanding SWAPSIZE to 2048 MB"
echo "###################################################################################################"


./set_SWAPSIZE.sh 2048

echo "###################################################################################################"
echo "SWAPSIZE expanded to 2048 MB. Preparing to install dependecies"
echo "###################################################################################################"

#Install necessary packages for OpenCV
sudo apt install -y build-essential cmake pkg-config
sudo apt install -y libjpeg-dev libtiff5-dev libjasper-dev libpng-dev

sudo apt install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt install -y libxvidcore-dev libx264-dev


sudo apt install -y libfontconfig1-dev libcairo2-dev
sudo apt install -y libgdk-pixbuf2.0-dev libpango1.0-dev
sudo apt install -y libgtk2.0-dev libgtk-3-dev

sudo apt install -y libatlas-base-dev gfortran

sudo apt install -y libhdf5-dev libhdf5-serial-dev libhdf5-103
sudo apt install -y libqt5gui5 libqt5webkit5 libqt5test5 python3-pyqt5

sudo apt install -y python3-dev

sudo apt-get install -y libcanberra-gtk-module libcanberra-gtk3-module

echo "###################################################################################################"
echo "All dependencies installed. Preparing to download opencv."
echo "###################################################################################################"



#Start OpenCv installation
cd ~

# Download
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.5.2.zip
wget -O opencv.zip https://github.com/opencv/opencv/archive/4.5.2.zip

# Unzip and rename folder
unzip opencv.zip
unzip opencv_contrib.zip

mv opencv-4.5.2 opencv
mv opencv_contrib-4.5.2 opencv_contrib

echo "###################################################################################################"
echo "Downloaded Opencv 4.5.2 and unzipped to folder opencv and opencv_contrib on root folder"
echo "###################################################################################################"


pip3 install numpy

echo "###################################################################################################"
echo "All pre-setup completed. OpenCV ready to build"
echo "###################################################################################################"


#Build files
cd opencv
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
    -D ENABLE_NEON=ON \
    -D ENABLE_VFPV3=ON \
    -D BUILD_TESTS=OFF \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D CMAKE_SHARED_LINKER_FLAGS=-latomic \
    -D BUILD_EXAMPLES=OFF ..


echo "###################################################################################################"
echo "Build completed, opencv ready to make. The make uses all 4 core of RP3, if the make stops inbetween or crashes change the -j4 to -j1 and delete build folder and repeat the steps from build"
echo "###################################################################################################"

#make using all core j4 and one core j1
make -j4


echo "###################################################################################################"
echo "Make done. Decreasing SWAPSIZE to 100 MB"
echo "###################################################################################################"


./set_SWAPSIZE.sh 100

echo "###################################################################################################"
echo "SWAPSIZE decrease to 100 MB. Installation complete checking is opencv is installed successfully"
echo "###################################################################################################"

# Check if OpenCV is installed in Python
if python -c "import cv2"; then
    echo "OpenCV is installed in Python"
else
    echo "OpenCV is not installed in Python"
fi

echo "###################################################################################################"
echo " "
echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Installation successful!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
echo " "
echo "###################################################################################################"
