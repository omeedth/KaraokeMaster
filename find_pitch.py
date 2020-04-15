from math import log2, pow

A4 = 440
C0 = A4*pow(2, -4.75)
name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    
def pitch(freq):
    h = round(12*log2(freq/C0))
    octave = h // 12
    n = h % 12
    return name[n] + str(octave)

### Important ###

# Frequencies of the strings
frequencies = {
	'E': 329.63,
	'A': 440,
	'D': 587.33,
	'G': 783.99,
	'B': 987.77,
	'e': 1318.5
}

### Testing ###

print(pitch(frequencies['e']))
