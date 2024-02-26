import sys
import json
from pathlib import Path
import os

#set module path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from triggerHandler import PIR


def main(config_path):

    with open(config_path, 'r') as config_file:
            config = json.load(config_file)


    myPIR = PIR(savepath=config['paths']['output'],pir_pin=config['pir']['gpioPin'])

    while True:
        myPIR.test_pir()
        logtime = time.strftime("%Y-%m-%d %H:%M:%S")
        # time.sleep(.1)


if __name__=="__main__":
    # run the camera test
    main(config_path='/home/pepper/MED4PEST/spyce-code/config/config.json')

