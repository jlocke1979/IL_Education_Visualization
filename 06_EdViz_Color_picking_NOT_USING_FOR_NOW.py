
"""THis file helps to choose colors between two given or three given points"""

# Source:http://bsou.io/posts/color-gradients-with-python

def hex_to_RGB(hex):
	''' "#FFFFFF" -> [255,255,255] '''
	# Pass 16 to the integer function for change of base
	return [int(hex[i:i+2], 16) for i in range(1,6,2)]


def RGB_to_hex(RGB):
	''' [255,255,255] -> "#FFFFFF" '''
  	# Components need to be integers for hex to make sense
	
	RGB = [int(x) for x in RGB]
	return "#"+"".join(["0{0:x}".format(v) if v < 16 else
	        "{0:x}".format(v) for v in RGB])





def color_dict(gradient):
	''' Takes in a list of RGB sub-lists and returns dictionary of
	colors in RGB and hex form for use in a graphing function
	defined later on '''
	return {"hex":[RGB_to_hex(RGB) for RGB in gradient],
	  "r":[RGB[0] for RGB in gradient],
	  "g":[RGB[1] for RGB in gradient],
	  "b":[RGB[2] for RGB in gradient]}


def linear_gradient(start_hex, finish_hex="#FFFFFF", n=10):
	''' returns a gradient list of (n) colors between
	two hex colors. start_hex and finish_hex
	should be the full six-digit color string,
	inlcuding the number sign ("#FFFFFF") '''
	# Starting and ending colors in RGB form
	s = hex_to_RGB(start_hex)
	f = hex_to_RGB(finish_hex)
	# Initilize a list of the output colors with the starting color
	RGB_list = [s]
	# Calcuate a color at each evenly spaced value of t from 1 to n
	for t in range(1, n):
		# Interpolate RGB vector for color at the current value of t
		curr_vector = [
	 		int(s[j] + (float(t)/(n-1))*(f[j]-s[j]))
	  		for j in range(3)
		]
		# Add it to our list of output colors
		RGB_list.append(curr_vector)

	return color_dict(RGB_list)




from numpy import random as rnd

def rand_hex_color(num=1):
	''' Generate random hex colors, default is one,
	  returning a string. If num is greater than
	  1, an array of strings is returned. '''
	colors = [
	RGB_to_hex([x*255 for x in rnd.rand(3)])
	for i in range(num)
	]
	if num == 1:
		return colors[0]
	else:
		return colors


def polylinear_gradient(colors, n):
	''' returns a list of colors forming linear gradients between
	  all sequential pairs of colors. "n" specifies the total
	  number of desired output colors '''
	# The number of colors per individual linear gradient
	n_out = int(float(n) / (len(colors) - 1))

	# returns dictionary defined by color_dict()
	gradient_dict = linear_gradient(colors[0], colors[1], n_out)

	if len(colors) > 1:
		for col in range(1, len(colors) - 1):
			next = linear_gradient(colors[col], colors[col+1], n_out)
	  		for k in ("hex", "r", "g", "b"):
	   			# Exclude first point to avoid duplicates
	   			gradient_dict[k] += next[k][1:]

	return gradient_dict



# Value cache
fact_cache = {}
def fact(n):
	''' Memoized factorial function '''
	try:
		return fact_cache[n]
	except(KeyError):
		if n == 1 or n == 0:
	  		result = 1
		else:
	  		result = n*fact(n-1)
			fact_cache[n] = result
		return result


def bernstein(t,n,i):
	''' Bernstein coefficient '''
	binom = fact(n)/float(fact(i)*fact(n - i))
	return binom*((1-t)**(n-i))*(t**i)


def bezier_gradient(colors, n_out=100):
	''' Returns a "bezier gradient" dictionary
	  using a given list of colors as control
	  points. Dictionary also contains control
	  colors/points. '''
	# RGB vectors for each color, use as control points
	RGB_list = [hex_to_RGB(color) for color in colors]
	n = len(RGB_list) - 1

	def bezier_interp(t):
		''' Define an interpolation function
		    for this specific curve'''
		# List of all summands
		summands = [
		  map(lambda x: int(bernstein(t,n,i)*x), c)
		  for i, c in enumerate(RGB_list)
		]
		# Output color
		out = [0,0,0]
		# Add components of each summand together
		for vector in summands:
		  for c in range(3):
		    out[c] += vector[c]
		return out

	gradient = [ bezier_interp(float(t)/(n_out-1)) for t in range(n_out)	]
	
	# Return all points requested for gradient
	return {
		"gradient": color_dict(gradient),
		"control": color_dict(RGB_list)
	}




# For plotting charts used in blog


from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def plot_gradient_series(color_dict, filename,
	         pointsize=100, control_points=None):
	''' Take a dictionary containing the color
	  gradient in RBG and hex form and plot
	  it to a 3D matplotlib device '''

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	xcol = color_dict["r"]
	ycol = color_dict["g"]
	zcol = color_dict["b"]

	# We can pass a vector of colors
	# corresponding to each point
	ax.scatter(xcol, ycol, zcol,
	         c=color_dict["hex"], s=pointsize)

	# If bezier control points passed to function,
	# plot along with curve
	if control_points != None:
		xcntl = control_points["r"]
		ycntl = control_points["g"]
		zcntl = control_points["b"]
		ax.scatter( xcntl, ycntl, zcntl,
	    	c=control_points["hex"],
	        s=pointsize, marker='s')

	ax.set_xlabel('Red Value')
	ax.set_ylabel('Green Value')
	ax.set_zlabel('Blue Value')
	ax.set_zlim3d(0,255)
	plt.ylim(0,255)
	plt.xlim(0,255)

	# Save two views of each plot
	ax.view_init(elev=15, azim=68)
	plt.savefig(filename + ".svg")
	ax.view_init(elev=15, azim=28)
	plt.savefig(filename + "_view_2.svg")

	# Show plot for test
	plt.show()
	return




# Testing by Justin
"""Run Test Functions"""
## Convert hex to RBG
# print hex_to_RGB('#ffffff')

## Convert RGB to hex
# print RGB_to_hex([255,255,255])

## Run linear gradient between two colors 
# print linear_gradient('#252525',"#FFFFFF", 5)

## Get a random Hex Color
# random_color_set = rand_hex_color(5)
# print = rand_hex_color(5)

## Run multiple linear gradient Polylinear interpolation
# random_color_set = rand_hex_color(5)
# print polylinear_gradient(random_color_set, 10)


## Run Non-linear Gradients 
# random_color_set = rand_hex_color(5)
# print random_color_set
# print bezier_gradient(random_color_set, 10)

# Run Matplotlib Graph

# plot_gradient_series()



""" Actual Implementation for Northerly """

####  Non-Linear Gradient for Northerly Chosen Color Scheme:
# selected_color_set = ['#00441b','#FFFFFF','#40004b']  # Green, White, Purple,
# results = bezier_gradient(selected_color_set, 3)
# print results
# plot_gradient_series(results['gradient'],"Test_output",100,results['control'])
#Conclusion Ends up with too much Gray"""



###### Try Using PolyLinear Function
selected_color_set = ['#00441b','#FFFFFF','#40004b']  # Green, White, Purple,
results = polylinear_gradient(selected_color_set, 13)
# Print in easy to read layout
for each in results['hex']:
	print each,"/",hex_to_RGB(each)




