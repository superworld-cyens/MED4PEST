import cv2
from datetime import datetime
import time
import os
from cv2 import VideoCapture, imwrite, createBackgroundSubtractorMOG2, countNonZero
from utils import log, Configuration, force_stop_camera
from threading import Thread, Lock

class CamMotion:
    def __init__(self, savepath, framerate, width, height, debug, camera_index=0, record_time=5):
        self.camera_index = camera_index
        self.debug = debug
        self.logpath = os.path.join(savepath, 'log')
        self.log = log(self.logpath)
        self.framerate = framerate
        self.record_time = record_time

        # Motion detection initialization
        self.bg_update_interval = 30  # in seconds, adjust as needed
        self.last_bg_update = time.time()
        self.bg_model_initialized = False
        self.fgbg = createBackgroundSubtractorMOG2(detectShadows=False)

        force_stop_camera()  # Quit all camera processes if open
        self.cam = VideoCapture(self.camera_index)
        if not self.cam.isOpened():
            raise Exception('Camera did not initialize, restart.')
        self.cam.set(3, width)
        self.cam.set(4, height)
        self.folderpath = savepath

        if not os.path.exists(self.logpath):
            os.mkdir(self.logpath)

        # Audio capture flags and timing
        self.audio_lock = Lock()
        self.last_audio_capture_time = time.time()
        self.audio_capture_initialized = False

    def test_camera(self):
        print("Press 'q' to exit the live feed.")
        while True:
            ret, frame = self.cam.read()
            if not ret:
                self.log.printDebug("Error: Can't receive frame (stream end?). Exiting ...", self.debug)
                print("Error: Can't receive frame (stream end?). Exiting ...")
                break
            cv2.imshow('Live Feed', frame)
            if cv2.waitKey(1) == ord('q'):
                break
        cv2.destroyAllWindows()

    def run(self, audio_class):
        while True:
            ret, frame = self.cam.read()
            if not ret:
                break

            # Check if background model needs to be updated
            dif_time = time.time() - self.last_bg_update
            if dif_time >= self.bg_update_interval:
                self.log.printDebug(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Commencing background refresh after {dif_time}...", self.debug)
                self.fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=True)
                self.last_bg_update = time.time()
                self.bg_model_initialized = False

            # Initialize background model for first 3 seconds
            if not self.bg_model_initialized:
                for _ in range(int(3 * self.framerate)):
                    ret, frame = self.cam.read()
                    fgmask = self.fgbg.apply(frame)
                    time.sleep(1 / self.framerate)
                self.bg_model_initialized = True

            # Apply background subtraction
            fgmask = self.fgbg.apply(frame)

            # Check if there is significant foreground (i.e., change from background)
            foreground_area = cv2.countNonZero(fgmask)
            total_area = frame.shape[0] * frame.shape[1]

            if foreground_area > 0.01 * total_area:
                # Save current frame to disk
                timestamp = datetime.now().strftime("%Y_%m_%d-%H_%M_%S-%f")
                output_dir_folder = os.path.join(self.folderpath, timestamp[:10], timestamp[11:16], 'image')
                filename = os.path.join(output_dir_folder, f"{timestamp}.png")
                if not os.path.exists(output_dir_folder):
                    os.makedirs(output_dir_folder)

                cv2.imwrite(filename, frame)
                self.log.printDebug(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Motion detected! Initiated file capture and storage protocol. File {filename} saved successfully.", self.debug)

                # Capture audio if not already initialized or if 60 seconds have passed since the last capture
                current_time = time.time()
                with self.audio_lock:
                    if not self.audio_capture_initialized or (current_time - self.last_audio_capture_time) >= 60:
                        self.audio_capture_initialized = True
                        self.last_audio_capture_time = current_time
                        audio_thread = Thread(target=audio_class.capture_audio)
                        audio_thread.start()

                # Print debug message if debug mode is on
                # if self.debug:
                #     cv2.imshow('frame', frame)
                #     cv2.imshow('fgmask', fgmask)

            # Check for quit key
            if cv2.waitKey(1) == ord('q'):
                break

        # Release video capture device and close all windows
        self.release_camera()

    def release_camera(self):
        self.cam.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # This is where you would initialize your audio class and start the CamMotion
    # Example:
    # audio_class = YourAudioClass()
    # cam_motion = CamMotion(savepath='./', framerate=30, width=640, height=480, debug=True)
    # cam_motion.run(audio_class)
    pass
