import numpy as np
import time
from datetime import datetime
from multiprocessing import Process
import os
import getpass
import json
import signal
from threading import Thread
from time import sleep


''' Import our .py files '''
# from Sensor import Sensors
# from AudioHandling import Audio
from cameraHandler import Camera
from audioHandler import Audio


class Controller():

    def __init__(self,config_path='./config/config.json'):
        
        #configure spyce
        self.spyceid = getpass.getuser()
        self.config_path = config_path
        self.config = self.__load_config__()


        #initialize camera
        # self.__initi_camera__()

        #initizlize audio
        self.__initi_audio__()
    
    

    def __initi_camera__(self):
        # initialize camera
        self.myCameras = Camera(savepath=self.config['paths']['output'], \
                            framerate=self.config['camera']['fps'], \
                            width=self.config['camera']['imageWidth'], \
                            height=self.config['camera']['imageHeight'], \
                            debug=self.config['settings']['debug'])
    
    def __initi_audio__(self):
        # initialize camera
        self.myAudio = Audio(savepath=self.config['paths']['output'], \
                        samplerate=self.config['audio']['samplerate'], \
                        channel=self.config['audio']['channel'])

    def run(self, trigger):
        pass


    def run_audiocam(self):
        #init camera, reason to put it here is reinitialize after each epoch
        self.__initi_camera__()
        process_list = []

        # Setup to handle SIGINT (Ctrl+C)
        original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
        record_time = self.config['settings']['record_time']

        if self.config['sensors']['audio']:
            proc_audio = Process(target=self.myAudio.capture_audio, args=(record_time,),name="AudioCaptureProcess")  # Assuming capture_audio method
            process_list.append(proc_audio)

        if self.config['sensors']['camera']:
            proc_cameras = Process(target=self.myCameras.capture_images, args=(record_time,),name="ImageCaptureProcess")
            process_list.append(proc_cameras)
    

        try:
            # Restore the original signal handler for graceful shutdown
            signal.signal(signal.SIGINT, original_sigint_handler)

            for process in process_list:
                process.start()

            # Start monitoring thread
            monitor_thread = Thread(target=self.monitor_processes, args=(process_list,))
            monitor_thread.start()

            for process in process_list:
                process.join()

            monitor_thread.join()  # Wait for the monitoring thread to finish
        except KeyboardInterrupt:
            print(f'{time.strftime("%Y-%m-%d %H:%M:%S")} Caught KeyboardInterrupt, terminating processes')
            for process in process_list:
                process.terminate()
            self.close()
        finally:
            for process in process_list:
                if process.is_alive():
                    process.join()
            self.close()

    def close(self):
        # Safely close camera, audio, and sensor
        if self.config['sensors']['camera']:
            self.myCameras.close_cameras() 
        if self.config['sensors']['audio']:
            self.myAudio.close_audio()  
        if self.config['sensors']['humtemp']:
            self.mySensor.close_sensor()  
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S")} Resources have been safely closed.')
    
    def monitor_processes(self, process_list):
        try:
            while True:
                all_finished = True
                for process in process_list:
                    if process.is_alive():
                        all_finished = False
                        print(f'{time.strftime("%Y-%m-%d %H:%M:%S")} Process {process.name} running.')
                    else:
                        print(f'{time.strftime("%Y-%m-%d %H:%M:%S")} Process {process.name} has completed.')
                if all_finished:
                    print(f'{time.strftime("%Y-%m-%d %H:%M:%S")} Run Audio-Camera processes has completed.')
                    break
                sleep(5)  # Wait for 1 second before checking again
        except Exception as e:
            print(f'{time.strftime("%Y-%m-%d %H:%M:%S")} Monitoring stopped due to an error: {e}')
    
    def __load_config__(self):
        with open(self.config_path, 'r') as config_file:
            return json.load(config_file)


if __name__ == "__main__":
    cont = Controller(config_path='./config/config.json')

    for count in range(0,2):
        cont.run_audiocam()
        # print(count)
        time.sleep(60)