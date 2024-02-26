import sys
import json
from pathlib import Path
import os

#set module path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from sensorHandler import ENVSensor


def main(config_path):

    with open(config_path, 'r') as config_file:
            config = json.load(config_file)


    mySensor = ENVSensor(savepath=config['paths']['output'])
    mySensor.test_envipara()

if __name__=="__main__":
    # run the camera test
    main(config_path='/home/pepper/MED4PEST/spyce-code/config/config.json')

