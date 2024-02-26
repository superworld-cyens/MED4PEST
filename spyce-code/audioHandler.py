import sounddevice as sd
import soundfile as sf
import simpleaudio as sa
import numpy as np
import scipy.io.wavfile as wav
from datetime import datetime
import os
import time


class Audio():


    def __init__(self, savepath, samplerate=384000, channel=1, device_index=None ):
        self.folderpath = savepath 
        self.samplerate = samplerate
        self.channel = channel #check if USB microphone is connected: arecord -l 
        self.device_index = device_index

    def capture_audio(self, record_time=5):
        recording = sd.rec(int(record_time * self.samplerate), samplerate=self.samplerate, channels=self.channel, device=self.device_index, dtype='float64')
        sd.wait()  # Wait until recording is finished

        #create save path from time 
        timestr = datetime.now()
        m_sec = round(timestr.microsecond / 1e6, 4)
        dateForFileName = timestr.strftime("%Y_%m_%d")
        timeForFileName = timestr.strftime("%H_%M")

        folderpath = f'{self.folderpath }/{dateForFileName}/{timeForFileName}/audio'
        if not(os.path.exists(folderpath)):
            os.makedirs(folderpath)

        fileName = os.path.join(folderpath, timestr.strftime(f"%H%M%S-{str(m_sec)[2:]}")+'.wav')
                    

        # wav.write(fileName, self.samplerate, np.int16(recording / np.max(np.abs(recording)) * 32767))
        sf.write(fileName, np.int16(recording / np.max(np.abs(recording)) * 32767),self.samplerate)

    def test_audio(self, duration=5):
        # Record audio
        logtime = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{logtime} Recording for {duration} seconds")
        recording = sd.rec(int(duration * self.samplerate), samplerate=self.samplerate, channels=self.channel, device=self.device_index, dtype='float32')
        sd.wait()  # Wait until recording is finished
        logtime = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{logtime} Recording stopped")

        # Save to a temporary folder
        temppath = './temp'
        if not(os.path.exists(temppath)):
            os.mkdir(temppath)
        logtime = time.strftime("%Y-%m-%d %H:%M:%S")
        sf.write(temppath+'/temp.wav', np.int16(recording / np.max(np.abs(recording)) * 32767), self.samplerate)
        print(f"{logtime} File saved, check temp folder")
    
    def close_audio(self):
        pass

if __name__=="__main__":
    rasp_aud = Audio(savepath="/home/pepper/data-store/testdata")
    start = datetime.now()
    rasp_aud.test_audio(duration=5)
    print(datetime.now()-start)
        