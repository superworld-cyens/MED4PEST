import numpy as np
import time
from datetime import datetime
from multiprocessing import Process
import os
import getpass
import json


''' Import our .py files '''
# from Sensor import Sensors
# from AudioHandling import Audio
from cameraHandler import Camera


class Controller():

    def __init__(self,config_path='./config/config.json'):
        
        #configure spyce
        self.spyceid = getpass.getuser()
        self.config_path = config_path
        self.config = self.__load_config__()
    

        #initialize camera
        self.__initi_camera__()
    
    

    def __initi_camera__(self):
        # initialize camera
        self.myCameras = Camera(savepath=self.config['paths']['output'], \
                            framerate=self.config['camera']['fps'], \
                            width=self.config['camera']['imageWidth'], \
                            height=self.config['camera']['imageHeight'], \
                            debug=self.config['settings']['debug'])


    def test_camera(self):
        # proc_cameras = Process(target = self.myCameras.capture_images, args=())
        
        # #start multiprocess
        # proc_cameras.start()

        # #wait till process finish
        # proc_cameras.join()

        self.myCameras.test_camera()
    
    def __load_config__(self):
        with open(self.config_path, 'r') as config_file:
            return json.load(config_file)


if __name__ == "__main__":
    cont = Controller()
    cont.test_camera()
