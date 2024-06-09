

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time



x = 0
y = 0
theta = 0
delta = 0.1
xdata , ydata = [], []

track_data = []

linear = [100]
angular = [0.75]
line, = plt.plot([], [], lw=2) 


v=100
w=0.75
for i in range(100):
	x = x + v*(np.cos(theta))*delta
	y = y + v*(np.sin(theta))*delta
	xdata.append(x)
	ydata.append(y)
	theta = theta + w
	theta = theta % 360
	#plt.xlim(25,50)
	#plt.ylim(-10,25)
	line.set_data(xdata, ydata) 
	plt.scatter(xdata,ydata, color = 'black', marker = (3,0,theta))
	#plt.clf()
	plt.pause(0.01)
	track_data.append((x, y , theta))
print(track_data)	
plt.show()


