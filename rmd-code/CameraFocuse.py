from cv2 import VideoCapture, imshow, destroyAllWindows, imwrite, waitKey
import time

cam = VideoCapture(0)
if not cam.isOpened():
    raise Exception('fuck. Camera did not initialise.')
cam.set(3, 800)
cam.set(4, 500)

i=0
while 1:
    ret, frame = cam.read()
    imshow("image", frame)
    print(i)
    i+=1
    waitKey(1)