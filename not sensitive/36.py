

class Circle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def distance_from_point(self, x, y):

        distance = math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

        if distance > self.r:

            angle = math.atan2(y - self.y, x - self.x)


            x_closest = self.x + self.r * math.cos(angle)
            y_closest = self.y + self.r * math.sin(angle)


            distance = math.sqrt((x - x_closest) ** 2 + (y - y_closest) ** 2)

        return distance

def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

track = Circle(1, 1, 9)


for i in range(200):
	
	
	error = track.distance_from_point(xdata[-1]+random.uniform(-2, 2), ydata[-1]+random.uniform(-2, 2))
	errors.append(error)
	
	d_error = (errors[i]-errors[i-1])/delta  # Derivative
	i_error = i_error*ki + 0.01*error*delta  #Integral
	
	v.append(error*kp + d_error*kd + i_error)
	w.append(w[i-1] + w[i]*delta)

	theta = w[-1]
	theta = theta % 360
	x = x + v[i]*(np.cos(theta))*delta
	y = y + v[i]*(np.sin(theta))*delta
	xdata.append(x)
	ydata.append(y)
	thetadata.append(theta)	
	
	
	
	line.set_data(xdata, ydata) 
	plt.scatter(xdata,ydata, color = 'black', marker = (3,0,theta))
	#plt.clf()
	plt.pause(0.0001)
	
plt.show()
		
        
