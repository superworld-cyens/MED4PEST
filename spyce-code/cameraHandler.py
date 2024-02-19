from cv2 import VideoCapture, imshow, destroyAllWindows, imwrite, imshow, waitKey
import time
import os

from logHandler import log


class Camera:

    def __init__(self, savepath, framerate=8, width=512, height=512, debug=True, logpath='./log'):
        self.debug = debug
        self.framerate = framerate
        self.cam = VideoCapture(0)
        if not self.cam.isOpened():
            self.printDebug('Camera did not initialise.', self.debug)
            raise Exception('Camera did not initialise, restart.')
        self.cam.set(3, width)
        self.cam.set(4, height)
        self.folderapth = savepath # still needs to add the name, now it has only the directory to be saved

        if not(os.path.exists(logpath)):
            os.mkdir(logpath)
        
        self.log = log('./log')

        
    def capture_images(self):
        try:
            missframecount = 0
            while True:
                startTime = time.time()
                ret, frame = self.cam.read()

                timeFPS = 1 / self.framerate # convertin framerate into waiting time in seconds between frames

                if (ret): #check if frames are captured successfully.
                    print(frame.shape)
                    # #recording time and preparing the folder
                    # timestr = time.strftime("%Y_%m_%d-%H%M%S")
                    # dateForFileName = time.strftime("%Y_%m_%d")

                    # os.mkdir(f'{self.imageName}/{dateForFileName}/')

                    # fileName = f'{self.imageName}/{dateForFileName}/{timestr} {i}.jpg'

                    # time.sleep(timeFPS)
                
                else:
                    e = "Cannot read frame."
                    self.log.printDebug(e, self.debug)
                    if missframecount<=self.framerate:
                        missframecount+=1
                    else:
                        e = f"Quiting after trying {self.framerate} frames."
                        self.log.printDebug(e, self.debug)
                        break
                

        # 
        # time_A = 0
        # elaspsedTime = 0
        # i = 0
        # try:
        #     while True:
                
#                 startTime = time.time()
#                 ret, frame = self.cam.read()
                
#                 timestr = time.strftime("%Y_%m_%d-%H%M%S")
#                 dateForFileName = time.strftime("%Y_%m_%d")
            
#                 #  test if it's night
#                 hour = timestr[-6:-4] # as string
#                 if hour[0] == '0':
#                     hour = int(hour[1])
#                 else:
#                     hour = int(hour)
                
#                 if time_A >= setTimeForA:
                    
#                     if ret:
#                         try:
#                             os.mkdir(f'{self.imageName}/{dateForFileName}/')
#                         except:
#                             pass
#                         fileName = f'{self.imageName}/{dateForFileName}/{timestr} {i}.jpg'
# #                         
#                         imwrite(fileName, frame)
#                     time_A = 0
#                     if i < self.framerate-1:
#                         i += 1
#                     else:
#                         i = 0
                
#                 elapsedTime = time.time() - startTime
#                 time_A = time_A + elapsedTime
#                 elaspsedTime = 0
        except Exception as e:
            self.log.printDebug(e, self.debug)
            self.closeAllCameras()
            
    # def printDebug(self, msg: str, debug: bool):
    #     if debug:
    #         print(msg)
    #         with open('./log/debug.txt', 'a') as f:
    #             f.write(f'{time.strftime("%Y-%m-%d %H:%M:%S")} - {msg}')
    #             f.write('\n')


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
        
        self.close_all_cameras()




    def close_all_cameras(self):
        self.cam.release()
        destroyAllWindows()


if __name__=="__main__":
    rsp_cam = Camera("/home/pepper/data-store")
    rsp_cam.captureImages()