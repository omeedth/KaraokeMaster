from math import log2, pow, sin, cos, atan2, sqrt, pi, fabs
import numpy as np
import matplotlib.pyplot as plt
import time

# https://betterexplained.com/articles/an-interactive-guide-to-the-fourier-transform/
# c_n  = INTEGRAL(0,1,e^(-2*PI*i*n*t) * f(t))

############################################################

# class Fourier():
#     def __init__(self):
#         pass

#     def transform(self, data):
#         # X_k = (1/N) * sum([x_n * e^(i * 2 * PI * k * (n/N)) for n in range(0,N)])
        
#         N = len(data)
#         frequencies = []
#         # points = [] # For Plotting

#         # All Frequencies
#         for frequency in range(0,N):
#             re = 0 # Real Part
#             im = 0 # Imaginary Part

#             # freq_points = []

#             for t in range(0, N):

#                 # Spin Signal Backwards
#                 rate = -1 * (2 * pi) * frequency

#                 # How Far Traveled at Time T
#                 time = t / N
#                 distance = rate * time

#                 # datapoint * e^(-i*2*pi*f) is complex, store each part
#                 re_part = data[t] * cos(distance)
#                 im_part = data[t] * sin(distance)

#                 # freq_points.append(im_part)

#                 # add this data point's contribution
#                 re += re_part
#                 im += im_part

#             # points.append(freq_points)

#             # Round to zero if close
#             if fabs(re) < 1E-10: re = 0
#             if fabs(im) < 1E-10: im = 0

#             # Average Contribution at this Frequency
#             re = re / N
#             im = im / N

#             frequencies.insert(frequency, {
#                 're': re,
#                 'im': im,
#                 'frequency': frequency,
#                 'amp': sqrt(re * re + im * im),
#                 'phase': atan2(im, re) * 180 / pi # in degrees
#             })

#         # print(points)
#         # list(map(lambda arr: plt.plot(arr), points))
#         # plt.show()

#         return frequencies

# f = Fourier()
# tr = f.transform([0, 1, 1, 1])
# waves = [[(tr[i]['amp'] * sin(tr[i]['frequency'] * theta)) for theta in np.arange(0,10,.05)] for i in range(len(tr))]
# list(map(lambda wave: plt.plot(wave), waves))
# plt.show()

############################################################

# hl, = plt.plot([], [])  

# X_AXIS_SIZE = 20
# STEP = 100
# RENDER_STEP = 10

# Y_MIN = -1
# Y_MAX = 1

# x = list(range(X_AXIS_SIZE * STEP))
# res = [0 for x in range(X_AXIS_SIZE * STEP)]

# plt.ion()
# fig, ax = plt.subplots()

# line, = ax.plot(x, res)
# ax.set_xlim([(X_AXIS_SIZE * STEP) - (STEP * 4),X_AXIS_SIZE * STEP])
# ax.set_ylim([Y_MIN,Y_MAX])

# num_frame = 1
# for x in range(X_AXIS_SIZE * STEP):

#     res.pop(0)
#     res.append(sin(x / STEP))

#     if num_frame % RENDER_STEP == 0:
#         line.set_ydata(res)
#         fig.canvas.draw()
#         fig.canvas.flush_events()

#     num_frame += 1

############################################################

try:
    # for Python2
    from Tkinter import *   ## notice capitalized T in Tkinter 
except ImportError:
    # for Python3
    from tkinter import *   ## notice lowercase 't' in tkinter here

# class CanvasWidget(Canvas):
#     def __init__(self,parent,width,height,spf,updateloop):
#         self.canvas = super().__init__(parent,width,height)        
#         self.spf = spf
#         self.events = []
#         self.begin()
#         self.updateloop = updateloop

#     # Additional Setup
#     def begin(self):
#         self.canvas.pack()   
    
#     def update(self):
#         self.canvas.delete("all") # Clear Canvas
#         self.updateloop()
#         self.canvas.after(self.spf,self.update)

# Time Keeping
SECOND = 1000       # in MS
fps = 30            # Frames Per Second
spf = SECOND // fps  # Seconds Per Frame

# Units
centerX = 50
centerY = 50
radius = 25
radians = 0
radStep = .05

# Saved Points
points = []

master = Tk()

w = Canvas(master, width=200, height=100)
w.pack()

def update():
    w.delete("all") # Clear Canvas
    w.create_oval(centerX - radius, centerY - radius, centerX + radius, centerY + radius)

    global radians 
    radians += radStep

    # Circle
    x = radius * cos(radians)
    y = radius * sin(radians)    
    w.create_line(centerX,centerY,centerX + x, centerY + y)

    # Optimization
    BUFF_SIZE = 250
    points.insert(0,y)
    if len(points) > BUFF_SIZE:
        points.pop()    

    # Wave
    i = 0
    startX = 100
    startY = 50
    while len(points) > (i + 1):
        w.create_line(startX + i, startY + points[i], startX + i + 1, startY + points[i+1])
        i += 1

    # Line to Wave
    w.create_line(centerX + x, centerY + y, startX, startY + points[0])

    w.after(spf,update)

update()

master = mainloop()

############################################################

# class circle():
#     def __init__(self, centerX, centerY, radius, frequency):
#         self.centerX = centerX
#         self.centerY = centerY
#         self.radius = radius
#         self.frequency = frequency

#     # polar to cartesian
#     def getCord(self, theta):
#         return (self.centerX + (self.radius * cos(theta)), (self.centerY + (self.radius * sin(theta))))

# # Time Keeping
# t = 0 # Radian of circle
# time_step = .05
# duration = 10

# # Circles
# c1 = circle(0,0,50,1)

# # Record Points
# xs = []
# ys = []

# def update():    

#     global t

#     point = c1.getCord(t)
#     xs.insert(0, point[0])
#     ys.insert(0, point[1])    

#     t += time_step


# while duration >= t:
#     update()

# plt.plot(xs,ys)
# plt.show()

# s1 = np.sin(np.arange(0,10,.1))
# s2 = np.sin(2 * np.arange(0,10,.1))

# plt.plot(s1)
# plt.plot(s2)
# plt.plot(s1 + s2)
# plt.show()

############################################################

# t = 10 # seconds (or whatever unit)
# step = 10 # steps per 1 unit of (t)
# y_data = list(map(lambda x: sin(x / step), range(t * step)))

# plt.plot(y_data)
# plt.show()
# print(y_data)

# for frame in range(t * step):
#     print(sin(frame/step))

# plt.ion()
# class DynamicUpdate():
#     #Suppose we know the x range
#     min_x = 0
#     max_x = 10

#     def on_launch(self):
#         #Set up plot
#         self.figure, self.ax = plt.subplots()
#         self.lines, = self.ax.plot([],[], 'o')
#         #Autoscale on unknown axis and known lims on the other
#         self.ax.set_autoscaley_on(True)
#         self.ax.set_xlim(self.min_x, self.max_x)
#         #Other stuff
#         self.ax.grid()
#         ...

#     def on_running(self, xdata, ydata):
#         #Update data (with the new _and_ the old points)
#         self.lines.set_xdata(xdata)
#         self.lines.set_ydata(ydata)
#         #Need both of these in order to rescale
#         self.ax.relim()
#         self.ax.autoscale_view()
#         #We need to draw *and* flush
#         self.figure.canvas.draw()
#         self.figure.canvas.flush_events()

#     #Example
#     def __call__(self):
#         import numpy as np
#         import time
#         # plt.ion()
#         self.on_launch()
#         xdata = []
#         ydata = []
#         for x in np.arange(0,10,0.5):
#             xdata.append(x)
#             ydata.append(np.exp(-x**2)+10*np.exp(-(x-7)**2))
#             self.on_running(xdata, ydata)
#             time.sleep(.1)
#         return xdata, ydata

# d = DynamicUpdate()
# d()