import RPi.GPIO as GPIO
import time

class PIR:
    def __init__(self, pir_pin=7, pulldown_resistor=False):
        # Ensure GPIO mode is set before setting up the pin
        GPIO.setmode(GPIO.BOARD)  # Consider moving this outside of the class if it fits your program structure better
        
        self.pir_pin = pir_pin
        GPIO.setup(self.pir_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # if pulldown_resistor:
        #     GPIO.setup(self.pir_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # else:
        # GPIO.cleanup()


    def capture_pir(self):
        # Simply read and return the PIR sensor state
        return GPIO.input(self.pir_pin)

    
    def test_pir(self):
        try:
            while True:
                
                pir_state = self.capture_pir()
                logtime = time.strftime("%Y-%m-%d %H:%M:%S")
                print(f"{logtime} {pir_state}")
                time.sleep(1)  # Add a small delay to prevent spamming your terminal
        except KeyboardInterrupt:
            logtime = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{logtime} Program terminated by user")
        finally:
            GPIO.cleanup()  # Clean up GPIO only once, here at the end


if __name__ == "__main__":
    rasp_pir = PIR()
    # GPIO.cleanup()
    # print(rasp_pir.capture_pir())
    rasp_pir.test_pir()
    