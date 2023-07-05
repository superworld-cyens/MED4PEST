import picamera
import datetime
import RPi.GPIO as GPIO
import pyaudio
import wave
import time
from RodentCountingObjectTracking import CountRodent()

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)
GPIO_PIR = [23, 22, 24]
for pin in GPIO_PIR:
    GPIO.setup(pin, GPIO.IN)

camera = picamera.PiCamera()
camera.start_preview()

p = pyaudio.PyAudio()

print("(PIR Module Test (CTRL-C to exit))")

Previous_State = [0, 0, 0]
Activation_Time = [0, 0, 0]

counter = CountRodent()

while True:
    if GPIO.input(23) == 1:
        now = datetime.datetime.now()
        image_filename = now.strftime("%Y-%m-%d-%H-%M-%S.jpg")
        audio_filename = now.strftime("%Y-%m-%d-%H-%M-%S.wav")

        camera.capture(image_filename)

        stream = p.open(format=pyaudio.paInt16,
                       channels=1,
                       rate=44100,
                       input=True,
                       frames_per_buffer=1024)

        frames = []

        for i in range(0, int(44100 / 1024 * 10)):
            data = stream.read(1024)
            frames.append(data)

        stream.stop_stream()
        stream.close()

        wf = wave.open(audio_filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))
        wf.close()

    Current_State = [GPIO.input(pin) for pin in GPIO_PIR]

    for i in range(len(Current_State)):
        if Current_State[i] == 1 and Previous_State[i] == 0:
            print("Motion detected on PIR ", i+1)
            Previous_State[i] = 1
            Activation_Time[i] = time.time()

            count = counter.count()
            print("Rodent Count: ", count)

            while time.time() - Activation_Time[i] < 300:
                Current_State[i] = GPIO.input(GPIO_PIR[i])

                if Current_State[i] == 1:
                    print("Motion detected on PIR ", i+1)
                    Activation_Time[i] = time.time()

                    count = counter.count()
                    print("Rodent Count: ", count)

                time.sleep(0.01)

            print("Sensor ", i+1, " is no longer active")
            Previous_State[i] = 0

        time.sleep(0.01)

GPIO.cleanup()