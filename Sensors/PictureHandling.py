from cv2 import VideoCapture, imshow, destroyAllWindows, imwrite
import time
import os


class Camera:

    def __init__(self, fileDirImages, framerate, width, height, startTimeVideo, endTimeVideo, debug):
        self.debug = debug
        self.framerate = framerate
        self.cam = VideoCapture(0)
        if not self.cam.isOpened():
            self.printDebug('Camera did not initialise.', self.debug)
            raise Exception('Camera did not initialise, restart.')
        self.cam.set(3, width)
        self.cam.set(4, height)
        self.imageName = fileDirImages # still needs to add the name, now it has only the directory to be saved
        self.startTimeVideo = startTimeVideo # what time will the camera start recording
        self.endTimeVideo = endTimeVideo # what time will the camera stop recording
        
    def captureImages(self):
        setTimeForA = 1 / self.framerate # convertin framerate into waiting time in seconds between frames
        time_A = 0
        elaspsedTime = 0
        i = 0
        try:
            while True:
                startTime = time.time()
                timestr = time.strftime("%Y_%m_%d-%H%M%S")
                dateForFileName = time.strftime("%Y_%m_%d")
            
                #  test if it's night
                hour = timestr[-6:-4] # as string
                if hour[0] == '0':
                    hour = int(hour[1])
                else:
                    hour = int(hour)
                    
                    
                if hour < self.startTimeVideo or hour > self.endTimeVideo:
                    continue
                    # if it's night then dont take pictures
                
                if time_A >= setTimeForA:
                    ret, frame = self.cam.read()
                    if ret:
                        try:
                            os.mkdir(f'{self.imageName}/{dateForFileName}/')
                        except:
                            pass
                        fileName = f'{self.imageName}/{dateForFileName}/{timestr} {i}.jpg'
#                         
                        imwrite(fileName, frame)
                    time_A = 0
                    if i < self.framerate-1:
                        i += 1
                    else:
                        i = 0
                
                elapsedTime = time.time() - startTime
                time_A = time_A + elapsedTime
                elaspsedTime = 0
        except Exception as e:
            self.printDebug(e, self.debug)
            self.closeAllCameras()
            
    def printDebug(self, msg: str, debug: bool):
        if debug:
            print(msg)
            with open('debug.txt', 'a') as f:
                f.write(f'{time.strftime("%Y_%m_%d-%H%M%S")} {msg}')
                f.write('\n')

    def closeAllCameras(self):
        self.cam.release()
        destroyAllWindows()
