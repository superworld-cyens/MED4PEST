#!/bin/bash

# Set the new swap size (in MB)
NEW_SWAP_SIZE=$1

# Edit the dphys-swapfile configuration file to set the new swap size
sudo sed -i "s/^CONF_SWAPSIZE=.*/CONF_SWAPSIZE=${NEW_SWAP_SIZE}/" /etc/dphys-swapfile

# Stop and restart the dphys-swapfile service to apply the new configuration
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start