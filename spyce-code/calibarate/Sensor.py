# Sensors handling class

# CircuitPython how to install guide: https://www.tomshardware.com/how-to/use-circuitpython-raspberry-pi

from gpiozero import CPUTemperature, MotionSensor # documentation: https://gpiozero.readthedocs.io/en/stable/index.html
from RPLCD.i2c import CharLCD # install with sudo pip3 install RPLCD
import adafruit_sht31d # install with sudo pip3 install adafruit-circuitpython-sht31d
import adafruit_ds1307 # install with sudo pip3 install adafruit-circuitpython-ds1307
from HX711 import SimpleHX711, Rate, Mass # to install follow this:
# git clone --depth=1 https://github.com/endail/hx711
# cd hx711
# sudo ./install-deps.sh
# make && sudo make install
# sudo pip3 install --upgrade hx711-rpi-py
import board
from time import sleep, gmtime, time, strftime  # , struct_time, localtime
import os
import csv
from os.path import exists
from subprocess import call

import requests


class Sensors:

    def __init__(self, debug):
        # constructor function
        # initialise all the sensors
        self.debug = debug
        self.cpuTemperatureSensor = self.initCPUTemperatureSensor()
        self.pirSensor = self.initPIRSensor()
        self.temperatureHumiditySensor = self.initTemperatureAndHumiditySensor()
        self.lcd = self.initLCD()
#         self.lcd.backlight_enabled = True
        self.rtc = self.initRTC()
        self.Temp = None
        self.Hum = None
        self.Mot = None
        self.Weig = None
        self.storage_warning_threshold = 90
        phoneNumner1 = 99999999
        phoneNumber2 = 99999999
        phoneNumber1Key = 999999
        phoneNumber2Key = 999999
        self.phone_numbers = [phoneNumner1, phoneNumner2] 
        self.api_keys = [phoneNumber1Key, phoneNumber1Key]
        
    
    ''' Getter functions '''
    def getTemperature(self):
        return round(self.temperatureHumiditySensor.temperature,1)

    def getHumidity(self):
        return round(self.temperatureHumiditySensor.relative_humidity,1)

    def getWeight(self):
        weight = 0
        with SimpleHX711(22, 27, -16, -229108) as hx:
            hx.setUnit(Mass.Unit.G)
            #hx.zero()
            try:
                weight = round(float(hx.weight(20)),1)
            except:
                self.printDebug('The weight sensor did not mange to give a value.', self.debug)
                weight = 0 # zero is an indication of an erroneus value
            #self.printDebug(f'{weight} Kg', self.debug)
        return weight

    def getMotion(self):
        # With the default queue_len of 1, this is effectively boolean where 0 means no motion detected and 1 means motion detected.
        # If you specify a queue_len greater than 1, this will be an averaged value where values closer to 1 imply motion detection.
        return self.pirSensor.value # or self.pirSensor.motion_detected

    def getCPU_Temperature(self):
        return round(self.cpuTemperatureSensor.temperature,1)
    
    def getTime(self):
        month = self.rtc.datetime.tm_mon
        day = self.rtc.datetime.tm_mday
        if month < 10:
            month = f'0{month}'
        if day < 10:
            day = f'0{day}'
        
        hour = self.rtc.datetime.tm_hour+3 # Correction to get Cyprus time
        if hour >= 24:
            hour = hour - 24
            
        return "{}/{}/{} {}:{:02}:{:02}".format(self.rtc.datetime.tm_year, month, day, hour, self.rtc.datetime.tm_min, self.rtc.datetime.tm_sec)
        
    def setLCD(self, msg):
        self.lcd.write_string(msg)

    def clearLCD(self):
        self.lcd.clear()

    ''' Initialisation functions '''       
    def initRTC(self):
        # Real Time Clock documentation: https://pypi.org/project/adafruit-circuitpython-ds1307/
        # UTC is Coordinated Universal Time (formerly known as Greenwich Mean Time, or GMT). The acronym UTC is not a mistake but a compromise between English and French.
        # The GMT time is used
        i2c = board.I2C()
        rtc = adafruit_ds1307.DS1307(i2c)
        rtc.datetime = gmtime()
        if rtc.datetime is None: # if you want to set the time to the time
            # displayed by the raspberry then change the if statement to
            # if rtc.datetime is not None:
            # run it once, and change it back to
            # if rtc.datetime is None:
            rtc.datetime = gmtime()
        return rtc
    
    def initLCD(self):
        # GND: Pin 6 (GND)
        # VCC: Pin 4 (5V)
        # SDA: Pin 3 (SDA)
        # SCL: Pin 5 (SCL)
        # Then create a new instance of the CharLCD class.
        # For that, you need to know the address of your LCD.
        # You can find it on the command line using the sudo i2cdetect 1 command (or sudo i2cdetect 0 on the original Raspberry Pi).
        # In my case the address of the display was 0x27.
        # You also need to provide the name of the I²C port expander that your board uses.
        # It should be written on the microchip that’s soldered on to your board.
        # Supported port expanders are the PCF8574, the MCP23008 and the MCP23017.
        # CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=20, rows=4, dotsize=8, charmap='A02', auto_linebreaks=True, backlight_enabled=True)
        lcd = CharLCD('PCF8574', 0x27)
        lcd.backlight_enabled = True
        self.printDebug('Succesfully initialized the LCD.', self.debug)
        return lcd
    
    def initTemperatureAndHumiditySensor(self):
        i2c = board.I2C()
        sensor = adafruit_sht31d.SHT31D(i2c)
        return sensor

    def initCPUTemperatureSensor(self):
        cpu = CPUTemperature()
        return cpu
    
    def initPIRSensor(self):
        # documentation: https://gpiozero.readthedocs.io/en/stable/api_input.html#motionsensor-d-sun-pir
        # Connect the PIR sensor’s pin labelled VCC to the 5V pin on the Raspberry Pi.
        # Connect the one labelled GND to a ground pin on the Pi.
        # Connect the one labelled OUT to any numbered GPIO pin on the Pi: GPIO 26.
        # This pin should be either pulled high or low. Also, I believe a logig level converter is needed to convert 5V to 3.3V.
        # pin=4, pull_up=False, active_state=None, queue_len=1, sample_rate=10, threshold=0.5, partial=False, pin_factory=None
        pir = MotionSensor(pin=26) # GPIO
        return pir

    ''' Close everything before shutting down the program '''
    def closeAllSensors(self):
        self.pirSensor.close()
        self.lcd.backlight_enabled = False
        self.lcd.close(clear=True)
        
    ''' Data handling functions that are user in audio class as well '''
    def populateLCD(self):
        strLCD = f'\rAT|H:{self.Temp}|{self.Hum}\n\rM|CT:{self.Mot}|{self.getCPU_Temperature()}\n\r{self.getTime()}\n\rW:{self.Weig}Kg' 
        self.clearLCD()
        self.setLCD(strLCD)

    def isHeaderSameLengthWithData(self, header: list, data: list):
        if len(header) == len(data):
            return True
        else:
            return False

    def isThereFile(self, fileName: str):
        return exists(fileName)
            
    def writeDataToCSV(self, header: list, data: list, fileName: str):
        fileExtention = '.csv'
        fileName = f'{fileName}{fileExtention}'
        try:
            if not self.isHeaderSameLengthWithData(header, data):
                self.printDebug('Error: Header and data have different length', self.debug)
                return
            
            if not self.isThereFile(fileName):
                myFile = open(fileName, 'w') # 'w' To create the file if it does not exist
                writer = csv.writer(myFile)
                writer.writerow(header)
                myFile.close()
            
            
            if len(data[0]) < 1000:
                with open(fileName, 'a') as myFile: # 'a' to append a new row at the end of the already existing file
                    writer = csv.writer(myFile)
                    writer.writerow(data)
                    #self.printDebug('Saved single line data.', self.debug)

            else:
                with open(fileName, 'a') as myFile: # 'a' to append a new row at the end of the already existing file
                    writer = csv.writer(myFile)
                    for d1, d2 in zip(data[0], data[1]):
                        writer.writerow([d1, d2])
                    #self.printDebug('Saved frequency domain data.', self.debug)
                
        except OSError as err:
            # There was a problem with opening the file
            self.printDebug("Error: OS error: {0}".format(err), self.debug)
            return
    
    def getDf(self):
        df = os.popen("df -h /dev/sda1")
        i = 0
        while True:
            i = i + 1
            line = df.readline()
            if i == 2:
                return(line.split()[0:6])
            
    def getStoragePercentage(self):
        disk_root = self.getDf()
        storage_now = int(disk_root[4][0:-1]) # -1 to remove the % symbol
        return storage_now
        
        
        
    def saveSensorData(self, header_A: list, header_B: list,
                         fileName_A: str, fileName_B: str,
                       saveTimeForA: int, saveTimeForB: int):
        
        if saveTimeForA/20 < 60:
            recordTimeForA = saveTimeForA
        else:
            recordTimeForA = saveTimeForA/20
        if saveTimeForB/20 < 60:
            recordTimeForB = saveTimeForB
        else:
            recordTimeForB = saveTimeForB/20
                        
        setTimeForLCDUpdate = 10 # in seconds
        setTimeForAirTempWarning = 30*60 # in seconds
        setTimeForCPUTempWarning = 20*60 # in seconds
        setTimeForStorageWarning = 24*60*60 # in seconds
        
        saveTimePassedForA = 0
        saveTimePassedForB = 0
        
        recordTimePassedForA = 0
        recordTimePassedForB = 0
        
        time_LCD_Update = 0
        time_AirTempWarning = 0
        time_CPUTempWarning = 0
        time_StorageWarning = 0
        
        cpu_temp = None
        
        counterForA = 0
        counterForB = 0

        sumForA = [0, 0, 0, 0] # temp, hum, motion, cpu temp
        sumForB = 0 # weight
        
        while True:
                
            startTime = time()
            if self.Temp is None:
                self.Temp = self.getTemperature()
            if self.Hum is None:   
                self.Hum = self.getHumidity()
            if self.Mot is None:
                self.Mot = self.getMotion()
            if self.Weig is None:
                self.Weig = self.getWeight()
            if cpu_temp is None:
                cpu_temp = self.getCPU_Temperature()
            elif cpu_temp > 65:
                cpu_temp = self.getCPU_Temperature()
            
            if cpu_temp > 75:            
                if time_CPUTempWarning >= setTimeForCPUTempWarning:
                    self.sendMessage(f'Warning:%20CPU%20Temperature%20{cpu_temp}%20Celcius.')
                    time_CPUTempWarning = 0
            
            if cpu_temp > 85:
                self.sendMessage(f'Shutting%20Down:%20CPU%20Temperature%20{cpu_temp}%20Celcius.')
                call("sudo shutdown -h now", shell=True)
                
            if time_StorageWarning >= setTimeForStorageWarning:
                storage_percentage_used = self.getStoragePercentage()
                if storage_percentage_used > self.storage_warning_threshold:
                    self.sendMessage(f'Warning: Storage almost full at {storage_percentage_used}% full.')
                else:
                    self.sendMessage(f'Update: Storage {storage_percentage_used}% full\nAirTemperature: {self.Temp} Celcius\nAirHumidity: {self.Hum}%\nMotion: {self.Mot}\nCPUTemperature: {cpu_temp} Celcius\n{self.getTime()}\nWeight: {self.Weig}Kg')
                time_StorageWarning = 0
            
            if self.Temp > 45:            
                if time_AirTempWarning >= setTimeForAirTempWarning:
                    self.sendMessage(f'Warning:%20Air%20Temperature%20{self.Temp}%20Celcius.')
                    time_AirTempWarning = 0
                    
            if recordTimePassedForA >= recordTimeForA:
                sumForA[0] += self.Temp
                sumForA[1] += self.Hum
                sumForA[2] += self.Mot
                sumForA[3] += cpu_temp
                counterForA += 1
                self.Temp = None
                self.Hum = None
                self.Mot = None
                cpu_temp = None
                #self.printDebug(f'sumForA: {sumForA}', self.debug)
                recordTimePassedForA = 0

            if recordTimePassedForB >= recordTimeForB:
                sumForB += self.Weig
                counterForB += 1
                self.Weig = None
                #self.printDebug(f'sumForB: {sumForB}', self.debug)
                recordTimePassedForB = 0
                
            if saveTimePassedForA >= saveTimeForA:
#                 if i read temperature in less than 5 min ago then sleep
                data_A = [self.getTime(), round(sumForA[0]/counterForA, 1), round(sumForA[1]/counterForA, 1), sumForA[2], round(sumForA[3]/counterForA, 1)]

                self.writeDataToCSV(header_A, data_A, fileName_A)
                counterForA = 0
                self.Temp = None
                self.Hum = None
                self.Mot = None
                cpu_temp = None
                sumForA = [0, 0, 0, 0]
                saveTimePassedForA = 0
            
            if saveTimePassedForB >= saveTimeForB:
#                 if i read weight in less than 10 min ago then sleep
                data_B = [self.getTime(), round(sumForB/counterForB, 3)]
                self.writeDataToCSV(header_B, data_B, fileName_B)
                counterForB = 0
                self.Weig = None
                sumForB = 0
                saveTimePassedForB = 0
            
            if time_LCD_Update >= setTimeForLCDUpdate:
                ''' Work the LCD for a bit '''
                self.populateLCD()
                time_LCD_Update = 0
            
            
            elapsedTime = time() - startTime
            time_LCD_Update += elapsedTime
            saveTimePassedForA += elapsedTime
            saveTimePassedForB += elapsedTime
            recordTimePassedForA += elapsedTime
            recordTimePassedForB += elapsedTime
            time_AirTempWarning += elapsedTime
            time_CPUTempWarning += elapsedTime
            time_StorageWarning += elapsedTime
            elapsedTime = 0

            
            
    def sendMessage(self, msg: str, phoneNumber=None, apiKey=None):
        try:
            if phoneNumber and apiKey is None:
                phoneNumber = self.phone_numbers
                apiKey = self.api_keys
            # https://www.callmebot.com/blog/free-api-whatsapp-messages/
            # 25 msg per 240 min
            for phone_number, api_key in zip(phoneNumber, apiKey):
                self.printDebug(f'Sending message to {phone_number}.', self.debug)
    #             https://api.callmebot.com/whatsapp.php?source=web&phone=+35799008615&apikey=105567&text=Warning:%20CPU%20Temperature%2050%20Celcius.
                requests.get(f'https://api.callmebot.com/whatsapp.php?source=web&phone=+{phone_number}&apikey={api_key}&text={msg}')
        except:
            self.printDebug('Didnt manage to send the whats up message.', self.debug)
            
    def printDebug(self, msg: str, debug: bool):
        if debug:
            print(msg)
            with open('debug.txt', 'a') as f:
                f.write(f'{strftime("%Y_%m_%d-%H%M%S")} {msg}')
                f.write('\n')


