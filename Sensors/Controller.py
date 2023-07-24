# Controller class, handling everything 

# To send messages use https://www.callmebot.com/blog/telegram-text-messages/

try:
    import numpy as np
    import time
    from datetime import datetime
    from multiprocessing import Process
    import os

    
    ''' Import our .py files '''
    from Sensor import Sensors
    from AudioHandling import Audio
    from PictureHandling import Camera
    
    hiveID = 'TEST'
    debug = True
    
    def printDebug(msg: str, debug: bool):
        if debug:
            print(msg)
            with open('debug.txt', 'a') as f:
                f.write(f'{time.strftime("%Y_%m_%d-%H%M%S")} {msg}')
                f.write('\n')
            
    
    ''' Try to connect to the WiFi '''
    wifiName = 'wifiname' 
    wifiPassword = 'password' 
    
    try:
        # This is not working yet
        os.system('sudo iwconfig wlan0 essid ' + wifiName + ' key ' + wifiPassword)
        printDebug('Successfuly connected to the WiFi', debug)
    except:
        for i in range(10):
            printDebug('Didnt connect to the wifi', debug)
    
    
    
    
    ''' Create the file directory that data will be saved into '''
    

    
    
    try:
        # If there is an external ssd then create there the file directories
        printDebug(f'found something {os.listdir("/media/pi")[0]}', debug)
        nameOfUSBStorage = os.listdir("/media/pi")[0]
        dataName = f'BeeHive-{hiveID}_'
        try:
            os.mkdir(f'/media/pi/{nameOfUSBStorage}/{dataName}Data/')
        except FileExistsError:
            printDebug("Directory Data on the SSD either already exists or it was not created.", debug)
            
        try:
            os.mkdir(f'/media/pi/{nameOfUSBStorage}/{dataName}Data/Images/')
        except FileExistsError:
            printDebug("Directory Data/Images on the SSD either already exists or it was not created.", debug)
        try:
            os.mkdir(f'/media/pi/{nameOfUSBStorage}/{dataName}Data/Audio/')
        except FileExistsError:
            printDebug("Directory Data/Audio on the SSD either already exists or it was not created.", debug)
            
        saveDir = f'/media/pi/{nameOfUSBStorage}'
    except Exception as e:
        printDebug('There is a usb connected but it is not a storage device.', debug)
        printDebug(e, debug)
        try:
            os.mkdir(f'/home/pi/Desktop/{dataName}Data/')
        except FileExistsError:
            printDebug("Directory Data on desktop either already exists or it was not created.", debug)
        
        try:
            os.mkdir(f'/home/pi/Desktop/{dataName}Data/Images/')
        except FileExistsError:
            printDebug("Directory Data/Images on desktop either already exists or it was not created.", debug)
        try:
            os.mkdir(f'/home/pi/Desktop/{dataName}Data/Audio/')
        except FileExistsError:
            printDebug("Directory Data/Audio on desktop either already exists or it was not created.", debug)
                        
        saveDir = '/home/pi/Desktop'
    
    ''' Setup the data '''
       
    # A: Audio
    # B: Temperature, Humidity, CPUTemperature, isThereMotion
    # C: Weight
    # D: Pictures
    
    fileDirImages = f'{saveDir}/{dataName}Data/Images'
    
    fileName_A = f'{saveDir}/{dataName}Data/Audio'
    header_A = ['Frequency', 'Amplitude'] # The time is in the name of the file

    fileName_B = f'{saveDir}/{dataName}Data/Data-A'
    header_B = ['Time', 'AirTemperature', 'AirHumidity', 'Motion', 'CPUTemp']

    fileName_C = f'{saveDir}/{dataName}Data/Data-B'
    header_C = ['Time', 'Weight']

    ''' Time intervals and duration for collecting data '''
    timeDurationAudio = 1 # seconds, collecting sound and saving it. The optimal time is calulated by trial and error
    timeIntervalTemperatureAndHumidity = 60*15 # seconds, every 15 minutes
    timeIntervalWeight = 60*60*2 # seconds, every 2 hours

    framerate = 6 # frames/sec
    imageWidth = 1280 # pixels
    imageHeight = 720 # pixels
    startTimeVideo = 7 # start recording images at 5 in the morning every day
    endTimeVideo = 17 # stop recording images at 20 in the night every day
    
    ''' Initialise the objects '''
    myCameras = Camera(fileDirImages, framerate, imageWidth, imageHeight, startTimeVideo, endTimeVideo, debug)
    mySensors = Sensors(debug)
    myAudio = Audio(mySensors, debug)
    phoneNumber = 99999999 # replace with correct one.
    phoneNumberID = 99999 # replace with correct one.
    
    mySensors.sendMessage('Successfuly initiated all 3 classes, and connected to the wifi.', phoneNumber, phoneNumberID)
    
    ''' Set the Processes '''
    ''' Capture images and saves to specified path with a specified fps'''
    proc_cameras = Process(target = myCameras.captureImages, args=())

    ''' Capture sound and save '''
    proc_audio = Process(target = myAudio.recordAudio, args=(timeDurationAudio, header_A,
                                                           fileName_A, timeDurationAudio+5))

    ''' Capture rest of sensors '''
    proc_sensors = Process(target = mySensors.saveSensorData, args=(header_B, header_C,
                                                                  fileName_B, fileName_C,
                                                                  timeIntervalTemperatureAndHumidity, timeIntervalWeight))

    ''' Start MultiProcessing '''
    
    proc_cameras.start()
    proc_audio.start()
    proc_sensors.start()
    
    ''' Wait for each process to end and then continue on with the rest of the code '''
    proc_cameras.join()
    proc_audio.join()
    proc_sensors.join()
  
        
except Exception as e:
    mySensors.closeAllSensors()
    myAudio.closeAllSensors()
    myCameras.closeAllCameras()
    printDebug("Closed from the exception.", debug)
    printDebug(e, debug)

except KeyboardInterrupt:
    proc_cameras.terminate()
    proc_audio.terminate()
    proc_sensors.terminate()
    mySensors.closeAllSensors()
    myAudio.closeAllSensors()
    myCameras.closeAllCameras()
    printDebug("KeyboardInterrupt caught", debug)
    
else:
    mySensors.closeAllSensors()
    myAudio.closeAllSensors()
    myCameras.closeAllCameras()
    printDebug("Closed from the finally.", debug)
