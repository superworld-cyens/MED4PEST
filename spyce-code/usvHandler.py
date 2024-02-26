import RPi.GPIO as GPIO
import time

class USV():

    def __init__(self,savepath, trig_pin, echo_pin):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
    

    def capture_usv(self):
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
        distance = (elapsed_time * 34300) / 2
        
        return distance
    
    def test_usv(self):
        print(self.capture_usv())


if __name__ == "__main__":
    rasp_usv = USV(savepath='./', trig_pin=7, echo_pin=11)
    rasp_usv.capture_usv()
    