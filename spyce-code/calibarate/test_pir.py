import RPi.GPIO as GPIO
import time

# Use GPIO numbering
GPIO.setmode(GPIO.BOARD)

# Pin 7 is connected to the PIR sensor output
pir_pin = 7

# Set pin 7 as an input pin with a pull-down resistor
GPIO.setup(pir_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("PIR Module Test (CTRL+C to exit)")

try:
    while True:
        # Read the state of the pin
        print(GPIO.input(pir_pin))
        if GPIO.input(pir_pin):
            # Motion detected
            logtime = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f'{logtime} - Motion detected!')
            # Wait a bit to avoid flooding messages
            time.sleep(1)
        else:
            # No motion detected
            time.sleep(0.1)
except KeyboardInterrupt:
    print("Program terminated")
finally:
    GPIO.cleanup()
