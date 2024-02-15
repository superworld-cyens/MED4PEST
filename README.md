# SPYCE [SPY-miCE] – An IoT smart sensor-trap station to monitor rodent 
![pexels-monique-laats-736524](https://github.com/superworld-cyens/MED4PEST/assets/37176779/b5764d20-93d1-4968-a0bd-91e48951ee55)


## Introduction

### MED4PEST Project: Ecologically-based rodent management
MED4PEST aims to develop proven, effective Ecologically Based Rodent Management (EBRM) methods and products, which are readily integrated into local pest /invasive rodent management systems in Mediterranean countries, contributing to the shift from synthetic pest control to biological and ecological pest management, ultimately leading to eco-sustainable farming systems, higher quality and quantity crop production and optimization of input use for ecosystem health. MED4PEST objectives and goals will produce new knowledge through scientific research that will be pursued with the collaborative research of the consortium partners from 2 Universities, 2 Research Institutes, and one company. <a href="https://med4pest.org/" target="_blank">MED4PEST</a>

## SPYCE - Rodent Monitoring Device
Collects temperature, humidity, sound, low frame rate video, and weight.

### Hardware
* Raspberry Pi 4
* Raspberry Pi Night Vision Camera
* M500-384 USB Ultrasound Microphone (Pettersson)
* Ultrasonic Distance Sensor - HC-SR04 (5V)
* SHT30 Temperature and Humidity Sensor (Waterproof)
* RadarIQ-M1 VISION Sensor (Additional)


Getting Started
    
Clone Repository:

    git clone https://github.com/superworld-cyens/MED4PEST.git

Dependencies:

    Python 3.7+
    OpenCV
    NumPy
    Matplotlib
    PiCamera
    Pyaudio
    

Install Dependencies:

    pip install -r spyce-setup/requirements.txt


Verifying Test Dependencies Installation:

After you have installed the packages listed in requirements.txt, it's important to ensure they are correctly installed. You can verify this by executing the following command:

    python spyce-setup/check_dependencies.py

This script checks each package and reports any issues with the installation process.

Troubleshooting Installation Issues:

If you encounter any problems with the installation of dependencies, please refer to the FAQ section at the end of this document for troubleshooting advice and common solutions.




FAQ:

1. Pip Installation Error
    * Error: externally-managed-environment
        × This environment is externally managed
        ╰─> To install Python packages system-wide, try apt install
            python3-xyz, where xyz is the package you are trying to
            install.

            If you wish to install a non-Debian-packaged Python package,
            create a virtual environment using python3 -m venv path/to/venv.
            Then use path/to/venv/bin/python and path/to/venv/bin/pip. Make
            sure you have python3-full installed.

            If you wish to install a non-Debian packaged Python application,
            it may be easiest to use pipx install xyz, which will manage a
            virtual environment for you. Make sure you have pipx installed.

            See /usr/share/doc/python3.11/README.venv for more information.

            note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.
            hint: See PEP 668 for the detailed specification.
    
    * Reason: Installation conflict between apt and pip packages.
        
    * Solution: Install the packages inside a python virtual environment.
        * sudo python3 -m venv path/to/virtual/env

            Example : python3 -m venv .venv 

        * source path/to/virtual/env

            Example : source .venv/bin/activate


2. When activating virtual environment 
    * Error: 'bash:/path/bin/activate: permission denied'
    * Reason: 'activate' script is not executable.
    * Solution: Make it chmod +x .venv/bin/activate



    


Acknowledgements

We would like to thank the following contributors for their help with this project:

  * @cpp
  * Shrasti Dadhich
  * Andreas Kamilaris
