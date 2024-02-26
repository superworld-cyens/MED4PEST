import RPi.GPIO as GPIO
import time

# Use GPIO numbers not pin numbers
GPIO.setmode(GPIO.BCM)

# pin numbers
TRIG = 7  # Change this based on your connections
ECHO = 11  # Change this based on your connections

# Set up the GPIO channels - one input, one output
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def detect_motion():
    # Ensure the trigger is set to low
    GPIO.output(TRIG, False)
    print("Waiting for sensor to settle")
    time.sleep(2)  # Waiting 2 seconds for the sensor to settle

    # Trigger the ultrasonic burst
    GPIO.output(TRIG, True)
    time.sleep(0.00001)  # Send pulse for 10 microseconds
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    # Here, rather than calculating distance, we're just noting a change indicating motion
    print("Motion detected")

try:
    while True:
        detect_motion()
        # Adding a delay to avoid constant triggering
        time.sleep(1)

except KeyboardInterrupt:
    print("Measurement stopped by User")

GPIO.cleanup()
