from colour import Color

########################### Testing of "Color Package"###################################################

"""Note - Help on Colour Package located here:
https://pypi.python.org/pypi/colour/0.1.1"""

# c = Color("blue")
# c.hsl
# c.red = 1
# c.saturation = 0.5
# c.luminance = 1 

# # print "%s" % c 

# red = Color("red")
# blue = Color("blue")
# print list(red.range_to(blue,5))

# black = Color("black")
# white = Color("white")

# print list(black.range_to(white,6))

# lime = Color("lime")
# print list(red.range_to(lime,5))


############################### Implementing Color Picker #########################
# print green.hsl 
# print white.hsl
# print green.luminance
# print white.luminance


# luminance_range = white.luminance - green.luminance 
# print luminance_range
# number_of_colors = 11.0
# luminance_interval = (luminance_range/ number_of_colors)
# print luminance_interval

# n = 1
# green_1 = green
# green_1.luminance = green.luminance + (luminance_interval * n) 
# print green_1.hex




def range_between_2_colors_altering_luminance(low_lum_color,high_lum_color,intervals):
	"""Defines a formulas that takes to colors and find the vcolors at equal intervals of luminance"""
	# test to see if luminance is equal
	if low_lum_color.luminance == high_lum_color.luminance:
		print "pick some different colors, their luminance are the exact same"

	# Calculate the distance between the luminance of the 2 colors, and figure out the interval needed (range/steps)
	luminance_range = high_lum_color.luminance - low_lum_color.luminance
	luminance_interval = luminance_range/ (intervals-1)

	color_array = ["%s" % low_lum_color]			# Initialize Color Array with Low Lum Color
	
	##### add all colors in between low and high 
	n = 1 											# initialize a counter for number of intervals
	initial_luminance = low_lum_color.luminance  	# set the starting luminance value (low)	
	while n < (intervals-1):						# iterate through the number of intervals (less 1 because we want to avoid starting and ending colors)
		low_lum_color.luminance = initial_luminance + n*luminance_interval
		color_array.append("%s" % low_lum_color)
		n +=1 
	color_array.append("%s" % high_lum_color) 		# Append the final ending color

	return color_array

def range_between_2_colors_altering_saturation(low_sat_color,high_sat_color,intervals):
	"""Defines a formulas that takes to colors and find the colors at equal intervals of saturation"""
	# test to see if Saturation is equal
	if low_sat_color.saturation == high_sat_color.saturation:
		print "pick some different colors, their saturation are the exact same"

	# Calculate the distance between the saturation of the 2 colors, and figure out the interval needed (range/steps)
	saturation_range = high_sat_color.saturation - low_sat_color.saturation
	saturation_interval = saturation_range/ (intervals-1)

	color_array = ["%s" % low_sat_color]			# Initialize Color Array with Low sat Color
	
	##### add all colors in between low and high 
	n = 1 											# initialize a counter for number of intervals
	initial_saturation = low_sat_color.saturation  	# set the starting luminance value (low)	
	while n < (intervals-1):						# iterate through the number of intervals (less 1 because we want to avoid starting and ending colors)
		low_sat_color.saturation = initial_saturation + n*saturation_interval
		color_array.append("%s" % low_sat_color)
		n +=1 
	color_array.append("%s" % high_sat_color) 		# Append the final ending color

	return color_array
# Establish Colors
deep_green = Color('#00441b')
pure_white = Color('#FFFFFF')
deep_purple = Color('#40004b')
color_set = [deep_green,pure_white,deep_purple] 

# Run scripts that create Colors
# print range_between_2_colors_altering_luminance(deep_green,pure_white,6)
# print range_between_2_colors_altering_saturation(deep_green,pure_white,6)

print range_between_2_colors_altering_luminance(deep_purple,pure_white,6)

