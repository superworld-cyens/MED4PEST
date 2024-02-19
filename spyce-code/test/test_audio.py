import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

def record_audio(duration=10, fs=48000, channels=1, device=None):
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=channels, device=device, dtype='float64')
    sd.wait()  # Wait until recording is finished
    print("Recording stopped")
    return recording

# Adjust these parameters as necessary
duration = 10  # seconds
fs = 192000  # sample rate
channels = 1  # mono recording
device_index = None  # None uses the default device, or use the index found with arecord -l

# Record audio
audio_data = record_audio(duration, fs, channels, device_index)

# Save the recording
output_filename = "recording.wav"
wav.write(output_filename, fs, np.int16(audio_data / np.max(np.abs(audio_data)) * 32767))
print(f"Audio saved to {output_filename}")
