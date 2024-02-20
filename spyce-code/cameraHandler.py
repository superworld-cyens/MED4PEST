from cv2 import VideoCapture, imshow, destroyAllWindows, imwrite, imshow, waitKey
import time
from datetime import datetime

import os

from logHandler import log


class Camera:

    def __init__(self, savepath, framerate=8, width=512, height=512, debug=True,device_index=0 , logpath='./log'):
        self.debug = debug
        self.log = log('./spyce-code/log')
        self.framerate = framerate
        self.cam = VideoCapture(device_index)
        if not self.cam.isOpened():
            self.log.printDebug('Camera did not initialise.', self.debug)
            raise Exception('Camera did not initialise, restart.')
        self.cam.set(3, width)
        self.cam.set(4, height)
        self.folderpath = savepath # still needs to add the name, now it has only the directory to be saved

        if not(os.path.exists(logpath)):
            os.mkdir(logpath)

        
    def capture_images(self, record_time=5):
        try:
            missframecount = 0
            t_zero = True
            startTime = time.time()
            while True:
                ret, frame = self.cam.read()

                timeFPS = 1 / self.framerate # convertin framerate into waiting time in seconds between frames

                if ret: #check if frames are captured successfully.
                    #recording time and preparing the folder
                    timestr = datetime.now()
                    m_sec = round(timestr.microsecond / 1e6, 4)
                    dateForFileName = timestr.strftime("%Y_%m_%d")
                    
                    #iamges are recorded in one folder for each acquistion
                    if t_zero==True:
                        timeForFileName = timestr.strftime("%H_%M")
                        t_zero = False
                        

                    folderpath = f'{self.folderpath }/{dateForFileName}/{timeForFileName}/image'
                    if not(os.path.exists(folderpath)):
                        os.makedirs(folderpath)

                    fileName = os.path.join(folderpath, timestr.strftime(f"%H%M%S-{str(m_sec)[2:]}")+'.png')
                    imwrite(fileName,frame)
                    time.sleep(timeFPS)
                
                else:
                    e = "Cannot read frame."
                    self.log.printDebug(e, self.debug)
                    if missframecount<=self.framerate:
                        missframecount+=1
                    else:
                        e = f"Quiting after trying {self.framerate} frames."
                        self.log.printDebug(e, self.debug)
                        self.close_cameras()
                        break
                # breaking after record time.
                if int(time.time()-startTime)>record_time:
                    self.close_cameras()
                    break
                
        except Exception as e:
            self.log.printDebug(e, self.debug)
            self.close_cameras()

    def test_camera(self):
        # Loop to continuously fetch frames from the camera feed
        while True:
            # Capture frame-by-frame
            ret, frame = self.cam.read()

            # If frame is read correctly ret is True
            if not ret:
                print("Error: Can't receive frame (stream end?). Exiting ...")
                break


            # print(frame.shape)
            # Display the resulting frame
            imshow('Camera Feed', frame)

            # Wait for the ESC key to be pressed to exit
            if waitKey(1) & 0xFF == 27:  # 27 is the ASCII code for the ESC key
                break
        
        self.close_cameras()


    def close_cameras(self):
        self.cam.release()
        destroyAllWindows()


if __name__=="__main__":
    rsp_cam = Camera("/home/pepper/data-store")
    rsp_cam.captureImages()