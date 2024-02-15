#!/bin/bash

# Set OpenCV version to install
OPENCV_VERSION='4.5.1'

# Update and upgrade system packages
sudo apt-get update && sudo apt-get upgrade -y

echo "###################################################################################################"
echo "Updated and Upgraded. Expanding SWAPSIZE to 2048 MB"
echo "###################################################################################################"


./set_SWAPSIZE.sh 2048

echo "###################################################################################################"
echo "SWAPSIZE expanded to 2048 MB. Preparing to install dependecies"
echo "###################################################################################################"

#Install necessary packages for OpenCV
sudo apt-get install -y build-essential cmake pkg-config unzip
sudo apt-get install -y libjpeg-dev libpng-dev libtiff-dev
sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install -y libxvidcore-dev libx264-dev
sudo apt-get install -y libgtk-3-dev
sudo apt-get install -y libatlas-base-dev gfortran
sudo apt-get install -y python3-dev

echo "###################################################################################################"
echo "All dependencies installed. Preparing to download opencv."
echo "###################################################################################################"



#Start OpenCv installation
cd ~

# Download
wget -O opencv.zip https://github.com/opencv/opencv/archive/${OPENCV_VERSION}.zip
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/${OPENCV_VERSION}.zip


# Unzip and rename folder
unzip opencv.zip
unzip opencv_contrib.zip

mv opencv-${OPENCV_VERSION} opencv
mv opencv_contrib-${OPENCV_VERSION} opencv_contrib

echo "###################################################################################################"
echo "Downloaded Opencv 4.5.2 and unzipped to folder opencv and opencv_contrib on root folder"
echo "###################################################################################################"


pip3 install numpy

echo "###################################################################################################"
echo "All pre-setup completed. OpenCV ready to build"
echo "###################################################################################################"


#Build files
cd ~/opencv
mkdir build
cd build

# Configure OpenCV build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D INSTALL_C_EXAMPLES=ON \
      -D INSTALL_PYTHON_EXAMPLES=ON \
      -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
      -D BUILD_EXAMPLES=ON ..


echo "###################################################################################################"
echo "Build completed, opencv ready to make. The make uses all 4 core of RP3, if the make stops inbetween or crashes change the -j4 to -j1 and delete build folder and repeat the steps from build"
echo "###################################################################################################"

#make using all core j4 and one core j1
make -j$(nproc)


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


# Cleanup (Optional)
cd ~
rm opencv.zip
rm opencv_contrib.zip
rm -rf opencv
rm -rf opencv_contrib

echo "###################################################################################################"
echo " "
echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Installation successful!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
echo " "
echo "###################################################################################################"
