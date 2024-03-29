# SPYCE [SPY-miCE] – An IoT Smart Sensor-Trap Station for Rodent Monitoring
![pexels-monique-laats-736524](https://github.com/superworld-cyens/MED4PEST/assets/37176779/b5764d20-93d1-4968-a0bd-91e48951ee55)

## Introduction

### MED4PEST Project: Ecologically-Based Rodent Management
MED4PEST aims to develop proven and effective Ecologically Based Rodent Management (EBRM) methods and products that can be readily integrated into local pest/invasive rodent management systems in Mediterranean countries. This initiative contributes to the shift from synthetic pest control to biological and ecological pest management, ultimately fostering eco-sustainable farming systems, enhancing crop production quality and quantity, and optimizing ecosystem health inputs. The MED4PEST objectives and goals will generate new knowledge through scientific research conducted in collaboration with consortium partners from two universities, two research institutes, and one company. [MED4PEST](https://med4pest.org/)

## SPYCE - Rodent Monitoring Device
The device collects data on temperature, humidity, sound, low frame rate video, and weight.

### Hardware
* Raspberry Pi 4
* Raspberry Pi Night Vision Camera
* M500-384 USB Ultrasound Microphone (Pettersson)
* Ultrasonic Distance Sensor - HC-SR04 (5V)
* SHT30 Temperature and Humidity Sensor (Waterproof)
* RadarIQ-M1 VISION Sensor (Additional)

## Getting Started

#### Install Raspberry Pi OS
Step 1: Download the Raspberry Pi Imager.

Step 2: Prepare the microSD Card.
1. Insert the microSD card into your computer’s card slot or into a USB card reader.
2. Open the Raspberry Pi Imager.
3. Click on "CHOOSE OS" and select the version of Raspberry Pi OS you prefer (e.g., Raspberry Pi OS Full, Raspberry Pi OS Lite for a headless setup, etc.).
4. Click on "CHOOSE SD CARD" and select your microSD card from the list.
5. Click on "WRITE" and wait for the process to complete. This will erase everything on the microSD card.

    Note: For standard practice, follow the instructions below:
    * In the Hostname field, type 'spyce'.
    * For the Username, enter your favorite spice (e.g., pepper, cumin, oregano, etc.).
    * Enter a password.
    * Enter the WiFi SSID and password (required for connecting to the Raspberry Pi in headless mode, i.e., via terminal).

#### Connecting to Raspberry Pi
1. **With a Monitor**: This is the simplest method and is recommended for beginners. Connect a monitor, keyboard, and mouse to work with the Raspberry Pi as a desktop setup.
2. **Using a Capture Card**.
3. **Via SSH**: This is the most efficient way to work with the Raspberry Pi. You can access the device without connecting any extra peripherals.

    Syntax:

        ssh username@hostname.local
        ssh pepper@spyce.local # Example
        ssh pepper@xx.x.xx.xx # Example
    
    Note: 
    1. For SSH connections to work, both devices need to be on the same network, typically due to network firewalls or security configurations. For remote access, consider using [remote.it](https://www.remote.it/getting-started/raspberry-pi).
    2. Consider using VSCode to connect to the raspberry pi (using SSH extension) [VSCode-SSH](https://code.visualstudio.com/docs/remote/ssh).

#### Update RPi Configuration

- Edit Raspberry Pi COnfigurations.

        sudo raspi-config
  
  In configuration, 
    
    - Advance Option > Expand Filesystem (Ensures that all of the SD card is available)
    - Interface Option > Legacy Camera > Enable
    - Interface Option > SSH > Enable
    - Interface Option > VNC > Enable
    - Interface Option > I2C > Enable
    - Interface Option > Serial Port > Enable
    - Interface Option > Remote GPIO > Enable

- Reboot the Rapberry Pi

#### Mounting Hardrive
- Create a mount point :  Create a folder where you want to mount your HDD.

        sudo mkdir -p /path/to/create/new_folder
        Ex: sudo mkdir -p /home/pepper/data-store

    This will create a folder in the give path.

- Identify the drive : Connect the HDD and run below command to the list block devices. 
            
        lsblk

    Look for your device, usually named something like /dev/sda1 for the first partition on the first detected USB HDD.

- Get UUID of HDD partition.

        blkid
    
    Look for UUID of your device.

- Auto-mounting using fstab.

        sudo nano /etc/fstab

- Add below line to fstab.

        UUID=your-uuid-here /mnt/myhdd auto defaults,nofail 0 0

        example: UUID=B696844C96840F55 /home/pepper/data-store auto defaults,nofail 0 0

- Reboot RPi to mount or run sudo mount -a




#### Install Dependencies
List of Dependencies:
- Adafruit-sht31d
- Board
- Numpy
- PyAudio
- OpenCV
- Sounddevice
- Soundfile
- Simpleaudio
- Scipy

To install the dependencies, follow the steps below:


1. Clone the repository:

        git clone https://github.com/superworld-cyens/MED4PEST.git

        Folder structure:
        /MED4PEST
        ├── spyce-code
        │ ├── calibarate
        │ └── config
        ├── spyce-resource
        ├── spyce-setup
        └── README.md

2. Update and upgrade the Raspberry Pi:

        sudo apt-get update

        sudo apt-get upgrade

3. Install the virtual environment, create a Python virtual environment, and activate it:

        sudo apt-get install python3-venv   # Install Python virtual environment package
        python -m venv .spy  # Create a virtual environment with any name
        source .spy/bin/activate  # Activate the virtual environment

4. Install dependency packages:

        sudo apt-get install build-essential cmake git pkg-config libjpeg-dev libtiff5-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev

        sudo apt-get install libhdf5-dev libhdf5-103

        sudo apt-get install libopenblas-dev

        sudo apt-get install libgtk2.0-dev pkg-config
        
        sudo apt-get install -y i2c-tools

        sudo apt-get screen

    Note: Ensure that the above dependency packages are installed correctly without any errors.

5. Install requirements:

        pip install -r spyce-setup/requirements.txt

6. ### You can run the below `setup_spyce.sh` script to automate the aforementioned steps:

        $chmod +x spyce-setup/setup.sh  # Make the file executable
        ./spyce-setup/setup.sh  # Execute the script

7. Verifying Test Dependencies Installation:

    After installing the packages listed in `requirements.txt`, verify the installation by executing the following script:

        python spyce-setup/check_dependencies.py

    This script checks each package and reports any issues with the installation process.

8. Troubleshooting Installation Issues:

    For troubleshooting advice and common solutions to installation issues, please refer to the FAQ section at the end of this document.

## How to run the code
- Navigate to code folder
    
        $cd spyce-code

- Update configuration setting on config.json
    
            "sensors":  {"camera"  : true,
                        "audio"   : true,
                        "humtemp" : false,
                        "weight"  : false}

            "settings": {"mode": 0,
                        "debug": true,
                        "record_time": 5,
                        "comment": "Mode 0 for PIR trigger, 1 for USS trigger, 2 for Camera trigger",
                        "output": "/home/pepper/data-store/testdata"}

            "camera":   {"fps":3,
                        "imageWidth":512, 
                        "imageHeight":512}

            "audio":    {"samplerate":384000,
                        "channel":1,
                        "comment": "Check if USB microphone is connected: arecord -l"
                        },
            
            "pir":      {"Data":13}
            
            "usv":      {"Trigger":7,
                        "Echo":11}
- To run the code it is adviced to use terminal multiplexer. 

    Note: Multiplexer allows users to start a screen session and then open any number of virtual terminals (or "windows") inside that session. Processes that run in Screen will continue to run when their window is not visible and even after the user disconnects.

        $screen


    Run the code

        python main.py

## Frequently Asked Questions

1. **Pip Installation Error**:
    - Error: `externally-managed-environment`
    - Reason: Installation conflict between `apt` and `pip` packages.
    - Solution: Install the packages inside a Python virtual environment.

2. **When activating the virtual environment**:
    - Error: `'bash:/path/bin/activate: permission denied'`.
    - Reason: The 'activate' script is not executable.
    - Solution: Make it executable.

3. **OpenCV not installed**:
    - Error: OpenCV cannot be installed using Pip due to compatibility issues.
    - Solution: Install OpenCV from the source file.

4. **While importing cv2, Numpy version error**
    - Error: Please note and check the following:
        * The Python version is: Python3.9 from "/usr/bin/  python"
        * The NumPy version is: "1.26.4"
        * from .cv2 import * ImportError: numpy.core.multiarray failed to import


    - Solution: pip3 install --upgrade pip, pip3 install --force-reinstall numpy

## Acknowledgements

We would like to thank the following contributors for their help with this project:

- Chirag Padubidri
- Shrasti Dadhich
- Andreas Kamilaris
