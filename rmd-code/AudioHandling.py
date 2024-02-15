# Audio handling class
import pyaudio #  sudo apt-get install python3-pyaudio
import numpy as np # pip3 install numpy==1.16.2
import time
from bokeh.plotting import figure, show # sudo pip3 install bokeh
from Sensor import Sensors
import os

class Audio:
    
    def __init__(self, sensorObject: object, debug: bool):
        self.debug = debug
        self.audioSensor = self.initAudioSensor()
        self.mySave = sensorObject
        self.samp_rate = 44100 # 44.1kHz sampling rate
        self.number = 1
        
    def getAudioSensor(self):
        return self.audioSensor
    
    def getIndexOfConnectedAudioDevices(self, audioObject, searchFor: str):
        for i in range(audioObject.get_device_count()):
            if searchFor in audioObject.get_device_info_by_index(i).get('name'):
                self.printDebug(f'Found the audio device specified {i}', self.debug)
                return i
        self.printDebug("Couldn't find the audio device specified", self.debug)
        return None
             
    def initAudioSensor(self):
        # The microphone: GEMBIRD MIC-C-01 CLIP-ON 3.5 MM
        # {
        #   Frequency response: 20Hz - 16kHz
        #   Sensitivity: -42dB+-2dB
        #   Output impetance: > 2.2k Ohm
        # } 
        # The new microphone: BOYA BY-MC2 USB Microphone
        # {
        #   Frequency response: 35Hz - 18kHz
        #   Sensitivity: -47dB+/-1dB/0dB=1V/Pa,1kHz
        #   Output impetance: 300 Ohm
        # }
        audioObject = pyaudio.PyAudio() # create pyaudio instantiation
        return audioObject
    
#-------------------------------------------------------------------------------------
    def recordAudio(self, recordingDuration: int, header: list, fileName: str, functionDuration: int):
        # recordingDuration in seconds
        form_1 = pyaudio.paInt16 # 16-bit resolution
        chans = 1 # 1 channel
        chunk = 4096 # 2^12 samples for buffer
        dev_index = self.getIndexOfConnectedAudioDevices(self.audioSensor, 'PDP Audio Device')
        mic_sens_dBV = -47.0
        if dev_index is None:
            dev_index = self.getIndexOfConnectedAudioDevices(self.audioSensor, 'Sound Blaster Play! 3') # device index found by p.get_device_info_by_index(ii)
            # mic sensitivity correction and bit conversion
            mic_sens_dBV = -42.0 # mic sensitivity in dBV + any gain
        mic_sens_corr = np.power(10.0,mic_sens_dBV/20.0) # calculate mic sensitivity conversion factor
        
        while 1:
            recordingName = time.strftime("%Y_%m_%d-%H%M%S")
            recordingFileName = time.strftime("%Y_%m_%d")
            
            stream = self.audioSensor.open(format=form_1,
                                rate=self.samp_rate,
                                channels=chans,
                                input_device_index=dev_index,
                                input=True,
                                frames_per_buffer=chunk
                               )

            frames = []
            startTime = time.time() # this doesnt need to be the actual time, it is just a time reference
            for i in range(0, int((self.samp_rate/chunk)*recordingDuration)):
                data = np.frombuffer(stream.read(chunk, exception_on_overflow = False), 'int16')
                data = ((data/np.power(2.0,15))*5.25)*(mic_sens_corr)
                frames.extend(data)
            
            stream.stop_stream()
            stream.close()
            #self.printDebug('Finished recording.', self.debug)

            # Rounnd each individual sample (tihs is about 3 orders of magnitude faster than using the round function in a for loop)
            roundedFrames = np.around(frames, 5)

            fourieredFrames = self.doFourierTransform(roundedFrames)
            # Each time a recording is made, save the frequency domain to a new csv file.
            try:
                os.mkdir(f'{fileName}/{recordingFileName}/')
            except:
                pass
            finalFileName = f'{fileName}/{recordingFileName}/{recordingName}'
            self.saveToCSVTheAudio(fourieredFrames, header, finalFileName)
            self.number += 1
            
            restingTime = functionDuration - (time.time()-startTime)
            if restingTime < 0:
                restingTime = 0
                self.printDebug('I need more time!', self.debug)
            time.sleep(restingTime)
            #self.printDebug('Finished from audio recording function.', self.debug)
        
    def saveToCSVTheAudio(self, recordingData: list, header: list, fileName: str):
        '''
        This is used for saving the top amplitude and corresponding frequency only
        data = [self.mySave.getTime(), recordingData[0][0], recordingData[0][1]] 
        '''

        # frequency, amplitude
        self.mySave.writeDataToCSV(header, recordingData, fileName)
        #self.printDebug('Saved the audio.', self.debug)
    
    def plotSound(self, soundAmplitude: list, duration: list):
        p = figure(title=f'Sound recording in seconds', x_axis_label='Duration', y_axis_label='Coefficient')
        p.line(y = soundAmplitude, x = duration, legend_label='0', line_width=2, color='orange')
        show(p, width=800, height=400)
        
    def doFourierTransform(self, samples: list, numberOfFrequenciesToReturn=5):  
        # Documentation: https://numpy.org/doc/stable/reference/generated/numpy.fft.fft.html
        # Documentaion 2: https://pythontic.com/visualization/signals/fouriertransform_fft
        fourierTransform = np.fft.fft(samples)/len(samples)           # Normalize samples
        # get the important info from the imaginary part and round the numpy array
        fourierTransform = np.around(abs(fourierTransform[range(int(len(samples)/2))]), 5) # Exclude sampling frequency
        tpCount     = len(samples)
        values      = np.arange(int(tpCount/2))
        timePeriod  = tpCount/self.samp_rate
        frequencies = np.around(values/timePeriod, 2)
        
        return [frequencies, fourierTransform] # returns the frequencies and the corresponding amplitude
        '''
        # Pick the dominand frequencies
        topFrequencies = np.argpartition(fourierTransform, -numberOfFrequenciesToReturn)[-numberOfFrequenciesToReturn:]
        # Banch together the top frequencies with the top amplitutes 
        dominandfrequenciesWithAmplitutes = [(frequencies[i], fourierTransform[i]) for i in topFrequencies]
        
        print(f'fourierTransform: len={len(fourierTransform)}')
        print(f'frequencies: len={len(frequencies)}')
        print(f'topFrequencies: len={len(topFrequencies)}, {topFrequencies}')

        return dominandfrequenciesWithAmplitutes '''
    
    def printDebug(self, msg: str, debug: bool):
        if debug:
            print(msg)
            with open('debug.txt', 'a') as f:
                f.write(f'{time.strftime("%Y_%m_%d-%H%M%S")} {msg}')
                f.write('\n')
        
    ### Close everything before shutting down the program ###
    def closeAllSensors(self):
        self.audioSensor.terminate()



