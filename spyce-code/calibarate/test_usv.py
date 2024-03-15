import sys
import json
from pathlib import Path
import os
import time

#set module path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from triggerHandler import USS


def main(config_path):

    with open(config_path, 'r') as config_file:
            config = json.load(config_file)


    mySensor = USS(savepath=config['paths']['output'], \
                trig_pin=config['uss']['Trigger'], \
                echo_pin=config['uss']['Echo'])
    while True:
        mySensor.test_usv()
        logtime = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{logtime} Testing the sensor working, To Quit 'Ctrl+C'")
        time.sleep(1)

if __name__=="__main__":
    # run the camera test
    main(config_path='/home/pepper/MED4PEST/spyce-code/config/config.json')

