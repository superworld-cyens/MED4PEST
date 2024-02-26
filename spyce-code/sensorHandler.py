import time
import board
import adafruit_sht31d
import csv
from datetime import datetime
import os
import RPi.GPIO as GPIO

class ENVSensor():

    def __init__(self, savepath):
        self.folderpath = savepath
        self.i2c = board.I2C()  # uses board.SCL and board.SDA
        self.sensor = adafruit_sht31d.SHT31D(self.i2c)

    
    def capture_envipara(self):
        try:
            temperature = self.sensor.temperature  # Temperature in degrees Celsius
            humidity = self.sensor.relative_humidity  # Relative Humidity in %

            timestr = datetime.now()
            # Formatting date and time for filename
            dateForFileName = timestr.strftime("%Y_%m_%d")
            timeForFileName = timestr.strftime("%H:%M:%S_%f")[:-3]  # Including milliseconds

            folderpath = f'{self.folderpath}/{dateForFileName}'
            if not os.path.exists(folderpath):
                os.makedirs(folderpath)
            
            filename = os.path.join(folderpath, f"{dateForFileName}.csv")

            # Check if file exists to write headers accordingly
            file_exists = os.path.isfile(filename)

            with open(filename, 'a') as file:
                # Write header if file is new
                if not file_exists:
                    file.write("Timestamp,Temperature (C),Humidity (%)\n")
                
                # Write data
                file.write(f"{dateForFileName} {timeForFileName},{temperature:.2f},{humidity:.2f}\n")

            print(f"Temperature: {temperature:.2f} C, Humidity: {humidity:.2f} %")
        
        except KeyboardInterrupt:
            logtime = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f'{logtime} Program stopped by user.')


    def test_envipara(self):
        try:
            while True:
                temperature = self.sensor.temperature  # Temperature in degrees Celsius
                humidity = self.sensor.relative_humidity  # Relative Humidity in %
                
                logtime = time.strftime("%Y-%m-%d %H:%M:%S")
                print(f"{logtime} Temperature: {temperature:.2f} C, Humidity: {humidity:.2f} %")
                
                # Wait for 2 seconds before reading again
                time.sleep(2)
        except KeyboardInterrupt:
            logtime = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f'{logtime} Program stopped by user.') 

if __name__=="__main__":
    rasp_sens = Sensor(savepath="/home/pepper/data-store/testdata")
    rasp_sens.capture_envipara()