import RPi.GPIO as GPIO
import time

class PIR:
    def __init__(self, savepath, pir_pin, pulldown_resistor=False):
        # Ensure GPIO mode is set before setting up the pin
        # GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)  # Consider moving this outside of the class if it fits your program structure better
        
        self.pir_pin = pir_pin
        GPIO.setup(self.pir_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # if pulldown_resistor:
        #     GPIO.setup(self.pir_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # else:
        # GPIO.cleanup()


    def capture_pir(self):
        # Return the PIR sensor state
        return GPIO.input(self.pir_pin)

    
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
        logtime = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{logtime} {self.capture_usv():.2f}cm")

if __name__ == "__main__":
    # rasp_pir = PIR(pir_pin=13,savepath='./')
    # rasp_pir.test_pir()

    rasp_usv = USV(savepath='./', trig_pin=7, echo_pin=11)
    rasp_usv.capture_usv()
    