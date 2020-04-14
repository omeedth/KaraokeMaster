import pyaudio # https://people.csail.mit.edu/hubert/pyaudio/docs/
import struct # https://docs.python.org/2/library/struct.html
import numpy as np
import matplotlib.pyplot as plt

CHUNK = 1024 * 4 # Size of individual piece of sound data in Bytes
FORMAT = pyaudio.paInt16 # Number of bits used  to stor the data (paInt16 = 16 bits) BIT DEPTH
CHANNELS = 1 # communication channel in which a sound signal is transported (1 = Monostereo)
RATE = 44100 # Converting from analog to digital signal is called sampling, and this is the Sample Rate per second

p = pyaudio.PyAudio()

chosen_device_index = -1
for x in range(0,p.get_device_count()):
    info = p.get_device_info_by_index(x)
    # print(info)
    if info["name"] == "pulse":
        chosen_device_index = info["index"]
        print("Chosen index: ", chosen_device_index)

print(chosen_device_index)

stream = p.open(format=FORMAT,
 channels=CHANNELS,
 rate=RATE,
 input_device_index=chosen_device_index,
 input=True,
 output=True,
 frames_per_buffer=CHUNK
 )
 
plt.ion()
fig, ax = plt.subplots()

x = np.arange(0, CHUNK)
data = stream.read(CHUNK)
data_int16 = struct.unpack(str(CHUNK) + 'h', data)
line, = ax.plot(x, data_int16)
#ax.set_xlim([xmin,xmax])
ax.set_ylim([-2**15,(2**15)-1])

while True:
 data = struct.unpack(str(CHUNK) + 'h', stream.read(CHUNK))
 line.set_ydata(data)
 fig.canvas.draw()
 fig.canvas.flush_events()