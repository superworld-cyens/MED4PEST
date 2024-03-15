import RPi.GPIO as GPIO
import time
from datetime import datetime
import os

class PIR:
    def __init__(self, savepath, pir_pin, pulldown_resistor=False):
        # Ensure GPIO mode is set before setting up the pin
        self.folderpath = savepath
        GPIO.setmode(GPIO.BOARD)  # Consider moving this outside of the class if it fits your program structure better
        
        self.pir_pin = pir_pin
        GPIO.setup(self.pir_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # if pulldown_resistor:
        #     GPIO.setup(self.pir_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # else:
        # GPIO.cleanup()


    def capture_pir(self, writedata=True):
        # Return the PIR sensor state
        pir_state = GPIO.input(self.pir_pin)
        if pir_state==1:
            self.__writedata__(pir_state)
            record_time=time.time()
        return pir_state

    
    def test_pir(self):
        try:
            while True:
                pir_state = self.capture_pir()
                logtime = time.strftime("%Y-%m-%d %H:%M:%S")
                if pir_state==1:
                    print(f"{logtime} Motion Detected! Testing the sensor working, To Quit 'Ctrl+C'")
                else:
                    print(f"{logtime} No Motion Detection! Testing the sensor working, To Quit 'Ctrl+C'")

                # print(f"{logtime} Testing the sensor working, To Quit 'Ctrl+C'")
                time.sleep(1)  # Add a small delay to prevent spamming your terminal
        except KeyboardInterrupt:
            logtime = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{logtime} Program terminated by user")
        finally:
            GPIO.cleanup()  # Clean up GPIO only once, here at the end
    
    def __writedata__(self, state):
        timestr = datetime.now()
        # Formatting date and time for filename
        dateForFileName = timestr.strftime("%Y_%m_%d")
        timeForFileName = timestr.strftime("%H:%M:%S_%f")[:-3]  # Including milliseconds

        folderpath = f'{self.folderpath}/{dateForFileName}'
        if not os.path.exists(folderpath):
            os.makedirs(folderpath)
        
        filename = os.path.join(folderpath, f"{dateForFileName}_pir.csv")

        # Check if file exists to write headers accordingly
        file_exists = os.path.isfile(filename)

        with open(filename, 'a') as file:
                # Write header if file is new
            if not file_exists:
                file.write("Timestamp, PIR State \n")
                
            # Write data
            file.write(f"{dateForFileName} {timeForFileName},{state}\n")


class USS():

    def __init__(self,savepath, trig_pin, echo_pin):
        self.folderpath = savepath
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

        #motion detetion variable
        self.calibarate_uss()
    

    def capture_usv(self,writedata=True):
        distance = self.get_distance()        
        usv_motion = self.__check_motion__(distance, writedata)

        return usv_motion
    
    def get_distance(self):
        GPIO.output(self.trig_pin, False)
        time.sleep(0.5)
        
        # Send a 10us pulse to start the measurement
        GPIO.output(self.trig_pin, True)
        time.sleep(0.00001)  # 10us pulse
        GPIO.output(self.trig_pin, False)
        
        # Initialize the start and stop times
        start_time = time.time()
        stop_time = start_time
        
        # Record the last low timestamp for start_time
        while GPIO.input(self.echo_pin) == 0:
            start_time = time.time()
        
        # Record the last high timestamp for stop_time
        while GPIO.input(self.echo_pin) == 1:
            stop_time = time.time()
        
        # Calculate the difference in timestamps
        elapsed_time = stop_time - start_time
        
        # Multiply by the speed of sound in cm/us and divide by 2 (back and forth)
        return (elapsed_time * 34300) / 2
    
    def test_usv(self):
        logtime = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{logtime} {self.get_distance():.2f}cm")
    
    def calibarate_uss(self):
        self.prev_distance = self.get_distance()
    
    def __check_motion__(self, cur_distance, thresh_distance=1,writedata=True,constant_bg=False):
        if abs(cur_distance-self.prev_distance)>=thresh_distance:
            logtime = time.strftime("%Y-%m-%d %H:%M:%S")
            motion = 1
        else:
            motion = 0
        
        if motion and writedata:
            self.__writedata__(self.prev_distance, cur_distance, motion)
        
        if not(constant_bg):
            self.prev_distance=cur_distance
        return motion
    
    def __writedata__(self, prevdistance, curdistance, motion):
        timestr = datetime.now()
        # Formatting date and time for filename
        dateForFileName = timestr.strftime("%Y_%m_%d")
        timeForFileName = timestr.strftime("%H:%M:%S_%f")[:-3]  # Including milliseconds

        folderpath = f'{self.folderpath}/{dateForFileName}'
        if not os.path.exists(folderpath):
            os.makedirs(folderpath)
        
        filename = os.path.join(folderpath, f"{dateForFileName}_uss.csv")

        # Check if file exists to write headers accordingly
        file_exists = os.path.isfile(filename)

        with open(filename, 'a') as file:
                # Write header if file is new
            if not file_exists:
                file.write("Timestamp, Previous_distance, Current_distance, Motion \n")
                
            # Write data
            file.write(f"{dateForFileName} {timeForFileName},{prevdistance}, {curdistance}, {motion}\n")


if __name__ == "__main__":
    # rasp_pir = PIR(pir_pin=13,savepath="/home/pepper/data-store/testdata")
    # while 1:
    #     rasp_pir.capture_pir()
    #     time.sleep(2)

    rasp_usv = USS(savepath="/home/pepper/data-store/testdata", trig_pin=7, echo_pin=11)
    while 1:
        print(rasp_usv.capture_usv())
    