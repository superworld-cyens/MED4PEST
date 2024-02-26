# import RPi.GPIO as GPIO
# import time

# # Set GPIO mode
# GPIO.setmode(GPIO.BOARD)

# # Define GPIO pins
# TRIG = 7
# ECHO = 11

# # Set up the GPIO channels - one input and one output
# GPIO.setup(TRIG, GPIO.OUT)
# GPIO.setup(ECHO, GPIO.IN)

# def get_distance():
#     # Ensure the trigger pin is low for a clean pulse
#     GPIO.output(TRIG, False)
#     time.sleep(0.5)
    
#     # Send a 10us pulse to start the measurement
#     GPIO.output(TRIG, True)
#     time.sleep(0.00001)  # 10us pulse
#     GPIO.output(TRIG, False)
    
#     # Initialize the start and stop times
#     start_time = time.time()
#     stop_time = start_time
    
#     # Record the last low timestamp for start_time
#     while GPIO.input(ECHO) == 0:
#         start_time = time.time()
    
#     # Record the last high timestamp for stop_time
#     while GPIO.input(ECHO) == 1:
#         stop_time = time.time()
    
#     # Calculate the difference in timestamps
#     elapsed_time = stop_time - start_time
    
#     # Multiply by the speed of sound in cm/us and divide by 2 (back and forth)
#     distance = (elapsed_time * 34300) / 2
    
#     return distance

# try:
#     while True:
#         distance = get_distance()
#         print(f"Distance: {distance:.2f}cm")
#         time.sleep(1)

# except KeyboardInterrupt:
#     print("Measurement stopped by user")
#     GPIO.cleanup()


import sys
import json
from pathlib import Path
import os
import time

#set module path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from triggerHandler import USV


def main(config_path):

    with open(config_path, 'r') as config_file:
            config = json.load(config_file)


    mySensor = USV(savepath=config['paths']['output'], \
                trig_pin=config['usv']['Trigger'], \
                echo_pin=config['usv']['Echo'])
    while True:
        mySensor.test_usv()
        logtime = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{logtime} Testing the sensor working, To Quit 'Ctrl+C'")
        time.sleep(1)

if __name__=="__main__":
    # run the camera test
    main(config_path='/home/pepper/MED4PEST/spyce-code/config/config.json')

