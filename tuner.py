from math import log2, pow

######################################################################
# https://newt.phys.unsw.edu.au/jw/notes.html - Citation

# n_0  =  log_2(f2/f1) - (Octave)
# f_n  =  2^n/12 * 440 Hz - (Frequency from A4)
# n  =  12*log2(fn/440 Hz) - (num of semitones from A4)
# n_o  =  log2(fn/440 Hz) - (number of octaves from A4)
# nc  =  1200*log2(fn/440 Hz) - (number of cents from A4)

# In electronic music, pitch is often given by MIDI number (m)
# m for note A4 = 69, and increases by one for each equal tempered semitone

# m  =  12*log2(fm/440 Hz) + 69
# f_m  =  2(m−69)/12(440 Hz)

# Cent - a logarithmic unit of measure used for musical intervals
# 12 semitones per Octave with 100 cents each

######################################################################
# A MIDI keyboard has 128 notes from 0 - 127
# FRAME_SIZE and FRAMES_PER_FFT to be powers of two.
# 20 Herz - 20,000 Herz -> Range of human hearing

NOTE_MIN = 0        # C_-1 - 0
NOTE_MAX = 127      # G_9 - 127
SAMPLE_RATE = 22050 # Sampling rate in Herz (Standard - 44100)
CHUNK = 1024 * 2    # Samples per frame
FRAMES_PER_FFT = 16 # ???

######################################################################

SAMPLES_PER_FFT = CHUNK*FRAMES_PER_FFT # ???
FREQ_STEP = float(SAMPLE_RATE)/SAMPLES_PER_FFT    # ???

######################################################################
# Reference notes used in the calculations

A4 = 440 # This will act as our reference note
C0 = A4 * pow(2, -4.75) # C0 is 4.75 octaves lower than A4

######################################################################
# Just for displaying note names

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

######################################################################
# Tuner Functions

''' Calculates the range between two notes (in Octaves) 
    Input: frequency1 (float), frequency2 (float)
    Output: Octave Range (float)
    NOTE: f1 can't be 0 (hopefully neither are 0)
'''
def octave_range(f1, f2):
    return log2(f2/f1)

''' Calculates the frequency of the note n semitones away from A4
    Input: n (float) - number of semitones after or before A4
    Output: Frequency (float)
'''
def note_from_A4(n):
    return pow(2, n/12) * A4

''' Calculates the frequency of the note n semitones away from reference frequency
    Input: n (float) - number of semitones after or before 'fr'
           fr (float) - frequency of a note to compare to
    Output: Frequency (float)
'''
def note_from_frequency(n,fr):
    return pow(2, n/12) * fr

''' Calculates number of semi-tones from A4
    Input: fn (float) - frequency (note)
    Output: number of semitones from A4 (float)
    NOTE: Can't be 0
'''
def num_semitones_from_A4(fn):
    return 12 * log2(fn / A4)

''' Calculates number of semi-tones from other frequency
    Input: fn (float) - frequency (note)
           fr (float) - frequency to compare from
    Output: number of semitones from relative frequency (float)
    NOTE: Can't be 0
'''
def num_semitones_from_frequency(fn, fr):
    return 12 * log2(fn / fr)

''' Calculates the range from A4 (in Octaves) 
    Input: frequency
    Output: Octave Range (float)
'''
def octaves_from_A4(fn):
    return log2(fn/A4)

''' Calculates the range from reference frequency (in Octaves) 
    Input: fn - frequency
           fr - reference frequency to compare from
    Output: Octave Range (float)
'''
def octaves_from_frequency(fn, fr):
    return log2(fn/fr)

''' Calculates the cents from A4 given frequency
    Input: frequency
    Output: cents (float)
'''
def cents_from_A4(fn):
    return 1200 * log2(fn / A4)

''' Calculates the cents from reference frequency given frequency
    Input: fn - frequency
           fr - reference frequency to compare to
    Output: cents (float)
'''
def cents_from_frequency(fn, fr):
    return 1200 * log2(fn / fr)

''' Calculates the MIDI value from frequency
    Input: frequency
    Output: MIDI value (float) (A4 = 69)
    NOTE: MIDI values should be integers if on tune
'''
def calculate_MIDI_value(fn):
    return 12 * log2(fn / A4) + 69

''' Calculates the frequency from MIDI value
    Input: MIDI value of note (A4 = 69)
    Output: frequency (float)
'''
def frequency_from_MIDI(m):
    return pow(2,(m-69)/12) * A4

'''
'''
def find_note_name(f):
    h = round(12 * log2(f / C0)) # number of half steps from C0
    n = h % 12
    return NOTE_NAMES[n]

'''
'''
def find_octave(f):
    h = round(12 * log2(f / C0)) # number of half steps from C0
    octave = h // 12
    return octave

'''
'''
def closest_note_to_frequency(f):
    m = round(calculate_MIDI_value(f))
    fr = frequency_from_MIDI(m)    
    cents = round(cents_from_frequency(f,fr))
    return fr,cents

######################################################################
# Testing Functions

# print(octave_range(A3,A4))
# print(note_from_A4(.9998603045752499))
# print(note_from_frequency(1,A4))
# print(num_semitones_from_A4(466.16))
# print(num_semitones_from_frequency(466.16,A4))
# print(octaves_from_A4(A3))
# print(octaves_from_frequency(A3,A4))
# print(cents_from_A4(A3))
# print(cents_from_frequency(A3,A4))
# print(calculate_MIDI_value(A3))
# print(frequency_from_MIDI(57))
# print(find_note_name(445))
# print(find_octave(445))
# print(closest_note_to_frequency(445))

######################################################################
# Usage

import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import struct # https://docs.python.org/2/library/struct.html

# Get min/max index within FFT of notes we care about.
# See docs for numpy.rfftfreq()
def note_to_fftbin(n): return frequency_from_MIDI(n)/FREQ_STEP
imin = max(0, int(np.floor(note_to_fftbin(NOTE_MIN-1))))
imax = min(SAMPLES_PER_FFT, int(np.ceil(note_to_fftbin(NOTE_MAX+1))))

# Allocate space to run an FFT. 
buf = np.zeros(SAMPLES_PER_FFT, dtype=np.float32)
num_frames = 0

# Initialize audio
stream = pyaudio.PyAudio().open(format=pyaudio.paInt16,
                                channels=1,
                                rate=SAMPLE_RATE,
                                input=True,
                                frames_per_buffer=CHUNK)

stream.start_stream()

# Setting up Plot
# plt.ion()
# fig, ax = plt.subplots()

# x = np.arange(0, CHUNK)
# data = stream.read(CHUNK)
# data_int16 = struct.unpack(str(CHUNK) + 'h', data)
# line, = ax.plot(x, data_int16)
# line = ax.plot(np.arange(32769 // 2), np.arange(32769 // 2))
# # ax.set_xlim([xmin,xmax])
# ax.set_ylim([-2**15,(2**15)-1])

# Create Hanning window function
window = 0.5 * (1 - np.cos(np.linspace(0, 2*np.pi, SAMPLES_PER_FFT, False)))

# Print initial text
print('sampling at', SAMPLE_RATE, 'Hz with max resolution of', FREQ_STEP, 'Hz')
print()

# As long as we are getting data:
while stream.is_active():

    # Uncertainty Principle - must have longer range of time to understand a frequency

    # Shift the buffer down and new data in
    buf[:-CHUNK] = buf[CHUNK:]
    buf[-CHUNK:] = np.frombuffer(stream.read(CHUNK), np.int16)

    # Run the FFT on the windowed buffer
    fft = np.fft.rfft(buf * window)

    # Get frequency of maximum response in range
    freq = (np.abs(fft[imin:imax]).argmax() + imin) * FREQ_STEP

    # Get note number and nearest note
    # n = freq_to_number(freq)
    n = calculate_MIDI_value(freq)
    n0 = int(round(n))

    # Console output once we have a full buffer
    num_frames += 1

    if num_frames >= FRAMES_PER_FFT:
        # pass
        print('freq: {:7.2f} Hz     note: {:>3s} {} {:+.2f}'.format(
            freq, find_note_name(freq),find_octave(freq),n-n0))