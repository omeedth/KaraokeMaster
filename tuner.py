from math import log2, pow

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

A4 = 440 # This will act as our reference note
C0 = A4 * pow(2, -4.75) # C0 is 4.75 octaves lower than A4

name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# A3 = 220 # Test Var

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

# TODO
def closest_note_to_frequency(f):
    h = round(12 * log2(f / C0)) # number of half steps from C0
    octave = h // 12
    n = h % 12
    fr = C0 * pow(2, h/12) # Closest Note's Frequency    
    remainder = round(cents_from_frequency(f,fr))
    return name[n] + str(octave) + ', ' + str(remainder) + ' cents'

### Tests ###

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
print(closest_note_to_frequency(A4))
