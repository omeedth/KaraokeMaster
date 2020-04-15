import numpy as np
import matplotlib.pyplot as plt

import math

import wave

import pyaudio

# Frequency and pitch describe the same thing,
# but from different viewpoints.
# FREQUENCY: measures the cycle rate of the physical waveform
# PITCH: how high or low it sounds when you hear it

# FREQUENCY is measured in HERTZ (Hz)
# AKA - number of waves per second
# FREQUENCY = SPEED / WAVELENGTH

# WAVELENGTH:  distance between two identical adjacent points in a wave
# Longer wavelength = lower pitches, 'height' of wave is the amplitude
# amplitude determines how loud a sound will be
# AKA - A full cycle
# Measured in METERS

# SPEED: how many wavelengths there are in some unit time
# SPEED = WAVELENGTH x FREQUENCY (S = Distance / Time)
# In terms of sound, it travels 343 meters per second at
# Standard Temperature and Pressure (STP) speed is constant

### Generate Sine Wave ###

start = 0
stop = 2*math.pi
increment = math.pi/20

time = np.arange(start,stop,increment)
amplitude = np.sin(time)

# plt.plot(time,amplitude)
# plt.show()

### Generate Sine Wave With Frequency and Sample Rate ###

# 𝐴 = Amplitude
# 𝜔 = Angular Frequency (radians/s)
# 𝜙 = Phase (radians)

# 𝑦 = 𝐴sin(𝜔𝑡+𝜙) = 𝐴sin(2𝜋𝑓𝑡+𝜙)

sample_rate = 44100 # how many samples per second
T = 1 / sample_rate # time per 1 sample
t = .1 # how long do we want to generate the signal
N = sample_rate * t # num of samples for duration of time 't'

frequency = 100 # herts (Hz)
omega = 2 * np.pi * frequency

t_seq = np.arange(N) * T # Multiply the sample number by Time per 1 sample to get the time over all samples

y = np.sin(omega * t_seq)

# plt.plot(t_seq,y)
# plt.show()

### Reading Wave File ###

file = wave.open('BassC2.wav')

print('Number of Channels:',file.getnchannels()) # if 2 channels every frame there are two samples 1 for each channel
print('Sampling Rate:',file.getframerate())
print('Sample Width:',file.getsampwidth()) # How many bytes are used to store a single sample
print('Frames:',file.getnframes()) 

### Accessing Audio Data ###

# file = wave.open('BassC2.wav')

T = 1 / file.getframerate()

t = file.getnframes() / file.getframerate()
print('Duration:',t)

# t_seq = np.arange(file.getnframes()) * T
# print(t_seq)

# rate, data = wave.read('BassC2.wav')
# data = file.readframes(1)
data = file.readframes(file.getnframes())
# print(data)

dt = np.dtype(np.int16)
wav_data = np.frombuffer(data, dtype=dt)
# print(wav_data[:2])

# print(str(len(t_seq)) + ':' + str(len(wav_data)))

# plt.plot(wav_data)
# plt.show()

### Playing Sound PyAudio ###

p = pyaudio.PyAudio()

volume = 0.5     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 1.0   # in seconds, may be float
f = 440.0        # sine frequency, Hz, may be float

# generate samples, note conversion to float32 array
samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

# play. May repeat with different volume values (if done interactively) 
stream.write(volume*samples)

stream.stop_stream()
stream.close()

p.terminate()