#### This script is 5 of 5 

# 1) reps the US_Census Data first           
# 2) Add GSA Data
# 3) Add IL REport Card Data                       
# 4) Clean the Data and do validation on it           
# 5) Summarize data and create holorpleth color boundaries.              <- This file



# Install Libraries
import geojson
import numpy as np
import math as math
import matplotlib.pyplot as plt
import copy



# # Store infiles 
secondary_districts_infile = "..\\output\\2017_secondary.geojson"
elementary_districts_infile = "..\\output\\2017_elementary.geojson"
unified_districts_infile = "..\\output\\2017_unified.geojson"

#  Min / Max / Mean Version 1
# THese are found using an input of an entire infile  (good for just unified, elementary, or secondary)

# Find the min of  field given a district infile
def find_min(infile,field_of_interest):	
	# Open files
	with open(infile) as f:
		district_file = geojson.load(f)
	# Cycle through file
	temp_storage = []
	for feature in district_file['features']:
		temp_storage.append(feature['properties'][field_of_interest])
	# find the min
	result = min(x for x in temp_storage if x is not None)
	# result = ceiling(result)
	return result


# find the min of an array
def find_min_2(array_of_values):
	min_2_result = min(x for x in array_of_values if x is not None)
	## Round it (uncomment if desired)
	# result = ceiling(result)
	return min_2_result


# Find the max of  field given a district infile
def find_max(infile,field_of_interest):
	# Open files
	with open(infile) as f:
		district_file = geojson.load(f)
	# Cycle through file
	temp_storage = []
	for feature in district_file['features']:
		temp_storage.append(feature['properties'][field_of_interest])
	
	result = np.nanmax(temp_storage)
	# result = ceiling(result)
	return result


# Find the Max of an array
def find_max_2(array_of_values):
	max_2_result = np.nanmax(array_of_values)
	## Round it (uncomment if desired)
	# result = ceiling(result)       
	return max_2_result

# Find the mean of field given a district infile
def find_mean(infile,field_of_interest):
	# Open files
	with open(infile) as f:
		district_file = geojson.load(f)
	# Cycle through file
	temp_storage = []
	for feature in district_file['features']:
		if isinstance(feature['properties'][field_of_interest],float):
			temp_storage.append(feature['properties'][field_of_interest])
		elif isinstance(feature['properties'][field_of_interest],int):
			temp_storage.append(feature['properties'][field_of_interest])
		else:
			pass


	# print temp_storage
	result = np.nanmean(temp_storage)
	# result = ceiling(result)
	return result

# Find the Mean of array
def find_mean_2(array_of_values):
	mean_2_result = np.nanmean(array_of_values)
	## Round it (uncomment if desired)
	# result = ceiling(result)
	return mean_2_result



# Open a district infile and store a specifid field of interest into an array.  Useful for running descriptive stats and histograms against array
def open_and_store_in_array(field_of_interest,infile):
	# Test Print 
	# print field_of_interest
	# print infile
	with open(infile) as f:
		working_file = geojson.load(f)
	array_result = []
	for feature in working_file['features']:
		if isinstance(feature['properties'][field_of_interest],float):
			# Test Print 
			# print ' It is a Float '
			array_result.append(feature['properties'][field_of_interest])
		elif isinstance(feature['properties'][field_of_interest],int):
			# Test Print 
			# print "It is a Int"
			array_result.append(feature['properties'][field_of_interest])
		else:
			# print "neither a float or int"
			pass
	# TEst Print
	# print array_result
	return array_result



# A function that joins that data of 3 different district types.  Frequently used for analysis of all 3 district types
def aggregate_3_district_infiles(field_of_interest,elementary_infile,secondary_infile,unified_infile):
	# Open files
	elementary_array = open_and_store_in_array(field_of_interest,elementary_infile)
	secondary_array = open_and_store_in_array(field_of_interest,secondary_infile)
	unified_array = open_and_store_in_array(field_of_interest,unified_infile)
	
	# Test Printing 
	# print "elementary_array"
	# print elementary_array
	# print "secondary_array"
	# print secondary_array
	# print "unified_array"
	# print unified_array
		

	# Cycle through file
	aggregate_array = []
	for each_elementary in elementary_array:
		aggregate_array.append(each_elementary) 
	for each_secondary in secondary_array:
		aggregate_array.append(each_secondary) 
	for each_unified in unified_array:
		aggregate_array.append(each_unified) 
	
	
	return aggregate_array


# A function that joins that data of 2 different district types.  Frequently used for Seconary & Unified (or Elementary and Unified)
def aggregate_2_district_infiles(field_of_interest,infile_1,infile_2):
	# Open files
	array1 = open_and_store_in_array(field_of_interest,infile_1)
	array2 = open_and_store_in_array(field_of_interest,infile_2)
	
	# Cycle through file
	aggregate_array = []
	for each_1 in array1:
		aggregate_array.append(each_1) 
	for each_2 in array2:
		aggregate_array.append(each_2) 
		
	return aggregate_array


# Function for rounding
def ceiling(x):
    n = int(x)
    return n if n-1 < x <= n else n+1


# Define a function that splits a range of numbers 
def split_range_into_equal_parts(min_value,max_value,number_of_splits):
	result = []
	stored_range = max_value-min_value
	increment = stored_range/number_of_splits
	i = 0
	while i < number_of_splits:
		result.append(ceiling(min_value+increment*i))			# Ceiling uses the function above to round off
		i+=1
	return result

   
# A function that  split  range into equal parts (given Min, max and number of splits)
def find_boundaries_equal_parts(infile,field_of_interest,number_of_splits):
	min_value = find_min(infile,field_of_interest)
	max_value = find_max(infile,field_of_interest)
	result = split_range_into_equal_parts(min_value,max_value,number_of_splits)
	return result



### Split Range into  Parts based on percentil  #####

def find_boundaries_percentiles(infile,field_of_interest,increments):
	result = [0]
	mean_value = find_mean(infile,field_of_interest)
	for percentile in increments:
		result.append(ceiling(mean_value+(mean_value*percentile)))
	# result.append(ceiling(find_max(infile,field_of_interest)))
	
	return result


### Split Range into  Parts based on a mean 

def find_boundaries_percentiles_mean_only(mean_value,increments):
	result = [0]
	for percentile in increments:
		result.append(ceiling(mean_value+(mean_value*percentile)))
	# result.append(ceiling(find_max(infile,field_of_interest)))
	return result


# Define a function that prints out basic statistics of given a field and district infile. 
def run_describe_infile(field_of_interest,infile):
	min_value = find_min(infile,field_of_interest)
	max_value = find_max(infile,field_of_interest)
	mean_value = find_mean(infile,field_of_interest)
	lower_percentile_boundary  = (find_min(infile,field_of_interest))/ (find_mean(infile,field_of_interest)) - 1 	
	upper_percentile_boundary  = (find_max(infile,field_of_interest))/ (find_mean(infile,field_of_interest)) - 1 
	print "Minimum = ", min_value 
	print "Maximum = ", max_value
	print "Mean = ", mean_value
	print "lower percentile boundary = ", lower_percentile_boundary
	print "upper percentile boundary = ", upper_percentile_boundary
	print ""
	return 

# Define a function that prints out basic statistics of given an array
def run_describe_array(array):
	min_value = find_min_2(array)
	max_value = find_max_2(array)
	mean_value = find_mean_2(array)
	lower_percentile_boundary  = (min_value/mean_value) - 1 	
	upper_percentile_boundary  = (max_value/mean_value) - 1 
	print "Minimum = ", min_value 
	print "Maximum = ", max_value
	print "Mean = ", mean_value
	print "lower percentile boundary = ", lower_percentile_boundary
	print "upper percentile boundary = ", upper_percentile_boundary
	print ""
	return 

# Prints out basic statistics for 3 district infiles and their aggregate 
def run_summary_script_all_districts(field_of_interest,elementary_infile,secondary_infile,unified_infile):
	print field_of_interest
	print "Elementary"
	print run_describe_infile(field_of_interest,elementary_infile)
	print "Secondary"
	print run_describe_infile(field_of_interest,secondary_infile)
	print "Unified"
	print run_describe_infile(field_of_interest,unified_infile)
	print "Combined"
	aggregate_array = aggregate_3_district_infiles(field_of_interest,elementary_infile,secondary_infile,unified_infile)
	print run_describe_array(aggregate_array)
	return


# Prints out basic statistics for 2 district infiles at once (Secondary and Unified...and their aggregate)
def run_summary_script_secondary_and_unified(field_of_interest,secondary_infile,unified_infile):
	print field_of_interest
	print "Secondary"
	print run_describe(field_of_interest,secondary_infile)
	print "Unified"
	print run_describe(field_of_interest,unified_infile)
	print "Combined"
	aggregate_array = aggregate_2_district_infiles(field_of_interest,secondary_infile,unified_infile)
	print run_describe_array(aggregate_array)

	return

# A Function that finds the boundaries of bins (using theory from Histograms).  
# This function is constrained by  maxiumum number of bins allows, an minimum number of occurrences within a bin 
# Takes in an array and returns the bins after satifying the given constrainst 
# This function sets the mean in the mid point of a bin (the goal of this is so when the color display ocurrs later it is known that this first bin represents the mean with some observations on either side)

def find_bin_boundaries_equal_distance_around_mean(data_array,max_number_of_bins, min_allowed_occurences_in_a_bin):
	# find basic statistics
	minimum_value = find_min_2(data_array)
	maximum_value = find_max_2(data_array)
	range_of_data = maximum_value - minimum_value
	count = len(data_array)
	mean = find_mean_2(data_array)
	minimum_percentile_below_mean = ((minimum_value / mean) - 1) 
	maximum_percentile_above_mean = ((maximum_value / mean) - 1)
	
	# initialize storage of bins 
	customized_bins = [minimum_value]

	########First Create the bin immediately arround the mean ( either side of mean using equal distance) ###########
	equal_bin_size_max = range_of_data/ max_number_of_bins
	mean_left_boundary = mean - (equal_bin_size_max/2)
	mean_right_boundary = mean + (equal_bin_size_max/2)

	##### Next do bins that are BELOW mean bin   (i.e. "left" of mean on a number line)############
	#Calculate the size of range below mean and number of bins needed (round them off to an integer)
	range_below_mean_bin = mean_left_boundary- minimum_value   
	intervals_below_mean =  range_below_mean_bin/equal_bin_size_max
	number_bins_below_mean_bin = math.trunc(intervals_below_mean)  
	
	# Create a while loop that runs on  each of the bin allowed below the mean
	next_left_bin_boundary = mean_left_boundary
	while number_bins_below_mean_bin > 0:
		next_left_bin_boundary = next_left_bin_boundary - (equal_bin_size_max)     # Set the bin boundary according to number of intervals away from mean 
		customized_bins.insert(1,next_left_bin_boundary)				# then Append (after min observation) to the customized bins array
		number_bins_below_mean_bin = number_bins_below_mean_bin -1 		# Then subtract 1 run and run through loop again if needed

	# Append the boundaries of the Mean Bins
	customized_bins.append(mean_left_boundary)
	customized_bins.append(mean_right_boundary)

	##### Finally do the bins that are ABOVE the mean bin ############
	range_above_mean_bin = maximum_value - mean_right_boundary 
	intervals_above_mean =  range_above_mean_bin/equal_bin_size_max
	number_bins_above_mean_bin = math.trunc(intervals_above_mean)  

	# Create a while loop that runs for however many intervals are needed
	number_of_itterations_b = 1 # initialize to 1 so 
	next_bin_boundary = mean_right_boundary
	while number_bins_above_mean_bin > 0:
		next_bin_boundary = next_bin_boundary + (number_of_itterations_b*equal_bin_size_max)     # Set the bin boundary according to number of intervals away from mean 
		customized_bins.append(next_bin_boundary)				# then Append to the customized bins array
		number_bins_above_mean_bin = number_bins_above_mean_bin -1 		# Then subtract 1 run and run through loop again if needed
		number_of_interations =+ 1

	# Append the final max value   (if needed).  
	# THe way the javascripts currently expect the data the maximum stop value isn't needed therefore commenting this out. 
	# customized_bins.append(maximum_value)

	# # Print Results for testing
	# print "Number of Bins = ", max_number_of_bins
	# # print "Count = ", count
	# # print "Minimum = ", minimum_value 
	# # # print "Maximum = ", maximum_value
	# print "Mean = ", mean	
	# # print "lower percentile boundary = ", minimum_percentile_below_mean
	# # print "upper percentile boundary = ", maximum_percentile_above_mean
	# print "Equal Bin Size Using Max Bins ", equal_bin_size_max
	# # print "Mean Left Boundary ", mean_left_boundary
	# # print "Mean Right Boundary ", mean_right_boundary
	# # print "Customized Bins", customized_bins

	return customized_bins,intervals_below_mean,intervals_above_mean


# A script for investigating the data and doing EDA.  RUns basic stats and prints histogram 
# Note - These histograms are accurate.  THe one originally done in EDA pythong script are note 
#(they counted each school as an observation...should have counted on districts. which this one does)

def describe_and_run_histogram_equal_bin_size_around_mean(data_array,max_number_of_bins,max_number_of_bins_below_mean,max_number_of_bins_above_mean, min_allowed_occurences_in_a_bin,field_description):
	#Find the customized Bin initially
	customized_bins,intervals_below_mean,intervals_above_mean = find_bin_boundaries_equal_distance_around_mean(data_array,max_number_of_bins, min_allowed_occurences_in_a_bin)
	# initialize number of bins to max number 
	current_number_of_bins = max_number_of_bins
	# Check to make sure we don't have too many bins above the mean, if so reduce by one until u get there
	while intervals_below_mean > max_number_of_bins_below_mean:
		current_number_of_bins = current_number_of_bins -1 
		customized_bins,intervals_below_mean,intervals_above_mean = find_bin_boundaries_equal_distance_around_mean(data_array,current_number_of_bins, min_allowed_occurences_in_a_bin)
	# Check to make sure we don't have too many bins below the mean, if so reduce by one until u get there
	while intervals_above_mean > max_number_of_bins_above_mean:
		current_number_of_bins = current_number_of_bins -1 
		customized_bins,intervals_below_mean,intervals_above_mean = find_bin_boundaries_equal_distance_around_mean(data_array,current_number_of_bins, min_allowed_occurences_in_a_bin)
	# Run Histogram initially
	n, bins, patches = plt.hist(data_array, bins = customized_bins, normed=0, facecolor='g', alpha=0.75)
	# check to make sure there is at least the required number of observations in a bin	
		# if there isn't enough observation in bin, then rerun making the number of bins 1 less
	while find_min_2(n) < min_allowed_occurences_in_a_bin:
		plt.clf()			# Clears the plot function
		current_number_of_bins = (current_number_of_bins-1)
		# Rerun the customized bins with the lower number of bins
		customized_bins = find_bin_boundaries_equal_distance_around_mean(data_array,current_number_of_bins, min_allowed_occurences_in_a_bin)
		n, bins, patches = plt.hist(data_array, bins =customized_bins, normed=0, facecolor='g', alpha=0.75)

	# Print out an array indicating the percentiles above or below mean (for reference)
	percentile_bins = []
	for each in customized_bins:
		value = ceiling(((each/ find_mean_2(data_array)) -1)*100)
		percentile_bins.append(value)
	print "bin boundaries: percentile "
	print percentile_bins

	# Print out the bin boundary for reference
	print "bin boundaries: values"
	print customized_bins

	# Programatically Set to Min Max of Data
	# xmin = find_min_2(data_array)
	# xmax = find_max_2(data_array)
	# ymin = ????
	# ymax = ?????
	# not sure how to do for ymin and ymax ....but manual mehtod is suitable
	
	# Manually Set to Min Max of Data
	# Note these value need updated by human depending on which field you print 
	xmin = 0
	xmax = 500000
	ymin = 1
	ymax = 350

	# Set Axes
	axes = plt.gca()
	axes.set_xlim([xmin,xmax])
	axes.set_ylim([ymin,ymax])

	# Print histogram for reference
	plt.xlabel(field_description)
	plt.ylabel('Frequency of occurrence')
	plt.title('Histogram of '+field_description)
	plt.axis()
	plt.grid(True)
	plt.show()
	
	return 


# Function that finds the minimum and maxium percentiles of a given field (used later for creating color legend)
def find_min_and_max_percentiles_all_districts(field_of_interest,elementary_infile,secondary_infile,unified_infile):
	
	elementary_lower_percentile = (find_min(elementary_infile,field_of_interest))/ (find_mean(elementary_infile,field_of_interest)) - 1 
	elementary_upper_percentile = (find_max(elementary_infile,field_of_interest))/ (find_mean(elementary_infile,field_of_interest)) - 1
	secondary_lower_percentile = (find_min(secondary_infile,field_of_interest))/ (find_mean(secondary_infile,field_of_interest)) - 1 
	secondary_upper_percentile = (find_max(secondary_infile,field_of_interest))/ (find_mean(secondary_infile,field_of_interest)) - 1 
	unified_lower_percentile = (find_min(unified_infile,field_of_interest))/ (find_mean(unified_infile,field_of_interest)) - 1 
	unified_upper_percentile = (find_max(unified_infile,field_of_interest))/ (find_mean(unified_infile,field_of_interest)) - 1 

	lower_array = [elementary_lower_percentile,secondary_lower_percentile,unified_lower_percentile]
	upper_array = [elementary_upper_percentile,secondary_upper_percentile,unified_upper_percentile]

	min_lower_percentile = find_min_2(lower_array)
	max_lower_percentile = find_max_2(upper_array)
	return [max_lower_percentile, min_lower_percentile]


def find_min_and_max_all_districts(field_of_interest,elementary_infile,secondary_infile,unified_infile):

	elementary_min = find_min(elementary_infile,field_of_interest)
	elementary_max = find_max(elementary_infile,field_of_interest)
	secondary_min = find_min(secondary_infile,field_of_interest)
	secondary_max = find_max(secondary_infile,field_of_interest)
	unified_min = find_min(unified_infile,field_of_interest)
	unified_max = find_max(unified_infile,field_of_interest)

	min_array = [elementary_min,secondary_min,unified_min]
	max_array = [elementary_max,secondary_max,unified_max]
	
	min_across_all_districts = find_min_2(min_array)
	max_across_all_districts = find_max_2(max_array)
	
	return [max_across_all_districts, min_across_all_districts]



# Function that find range given and array of a minimum and maximum percentil
def find_percentile_range(percentile_array):
	result = percentile_array[0] - percentile_array[1]
	return result


def helper_function_create_boundaries_diverging(district_result,district_left_of_mean,district_right_of_mean, \
	district_min_percentile,district_max_percentile,district_mean, \
	max_bins_below_mean,max_bins_above_mean,\
	district_rounded_bin_amount,round_to_nearest, percent_or_not):

	# print "District Mean "
	# print district_mean

	if percent_or_not == "percent":
		# do all the bins lower than mean 
		district_next_left_percentile_boundary = district_left_of_mean 	# initially set next left boundary as (left of Zero,,,i.e. zero = mean)
		track_bins_below = -1

		# print "district_next_left_percentile_boundary"
		# print district_next_left_percentile_boundary

		# print "district_min_percentile"
		# print district_min_percentile


		# Set all bins lower than the mean
		while district_next_left_percentile_boundary >= district_min_percentile:
			## Test Printing
			# print "Track Bins Below"
			# print track_bins_below
			# print "district_next_left_percentile_boundary"
			# print district_next_left_percentile_boundary

			if track_bins_below <= -max_bins_below_mean:  # Note This is INTENTIONALLY not parallel with if statement in next section.  THis is by design as the lower values must show up in stops,..but not higher ones                  
				break
			else:
 				district_result[track_bins_below] = {"percentile":(district_next_left_percentile_boundary- int(district_mean))}
				district_next_left_percentile_boundary = (district_next_left_percentile_boundary + - district_rounded_bin_amount)
				track_bins_below = track_bins_below-1
		
		#insert the lower boundary 
		district_result[track_bins_below] = {"percentile":(district_next_left_percentile_boundary-int(district_mean))}

		# then do all the bins higher than the mean		
		district_next_right_percentile_boundary  =  district_right_of_mean
		track_bins_above = 1


		# print "district_next_right_percentile_boundary"
		# print district_next_right_percentile_boundary
		# print "district_max_percentile"
		# print district_max_percentile

		while district_next_right_percentile_boundary <= district_max_percentile:

			#Test Printing 
			# print "track_bins_above"
			# print track_bins_above
			# print "district_next_right_percentile_boundary"
			# print district_next_right_percentile_boundary

			if track_bins_above > max_bins_above_mean:					
				break
			else:
				district_result[track_bins_above] = {"percentile":(district_next_right_percentile_boundary-int(district_mean))}	
				district_next_right_percentile_boundary = district_next_right_percentile_boundary + district_rounded_bin_amount
				track_bins_above = track_bins_above + 1
		pass
	
		# currently comment this section out...as we don't need a stop for max,..but if need uncomment in future
		# result[track_bins_below] = {'Percentile':round(district_max_percentile,round_to_nearest)}

	elif percent_or_not == "not_percent":
		# do all the bins lower than mean 
		district_next_left_percentile_boundary = district_left_of_mean 	# initially set next left boundary as (left of Zero,,,i.e. zero = mean)
		track_bins_below = -1

		# print "district_next_left_percentile_boundary"
		# print district_next_left_percentile_boundary

		# print "district_min_percentile"
		# print district_min_percentile


		# Set all bins lower than the mean
		while district_next_left_percentile_boundary >= district_min_percentile:
			## Test Printing
			# print "Track Bins Below"
			# print track_bins_below
			# print "district_next_left_percentile_boundary"
			# print district_next_left_percentile_boundary

			if track_bins_below <= -max_bins_below_mean:  # Note This is INTENTIONALLY not parallel with if statement in next section.  THis is by design as the lower values must show up in stops,..but not higher ones                  
				break
			else:
				district_result[track_bins_below] = {"percentile":round(district_next_left_percentile_boundary, round_to_nearest)}
				district_next_left_percentile_boundary = (district_next_left_percentile_boundary + - district_rounded_bin_amount)
				track_bins_below = track_bins_below-1
		
		#insert the lower boundary 
		district_result[track_bins_below] = {"percentile":round(district_min_percentile,round_to_nearest)}

		# then do all the bins higher than the mean		
		district_next_right_percentile_boundary  =  district_right_of_mean
		track_bins_above = 1


		# print "district_next_right_percentile_boundary"
		# print district_next_right_percentile_boundary
		# print "district_max_percentile"
		# print district_max_percentile

		while district_next_right_percentile_boundary <= district_max_percentile:

			# #Test Printing 
			# print "track_bins_above"
			# print track_bins_above
			# print "district_next_right_percentile_boundary"
			# print district_next_right_percentile_boundary

			if track_bins_above > max_bins_above_mean:					
				break
			else:
				district_result[track_bins_above] = {"percentile":round(district_next_right_percentile_boundary,round_to_nearest)}	
				district_next_right_percentile_boundary = district_next_right_percentile_boundary + district_rounded_bin_amount
				track_bins_above = track_bins_above + 1
		pass
	
		# currently comment this section out...as we don't need a stop for max,..but if need uncomment in future
		# result[track_bins_below] = {'Percentile':round(district_max_percentile,round_to_nearest)}
		pass
	else:
		print "error, set 'percent_or_not' to 'percent' or 'not_percent'"
		return
	

	# print "district_result"
	# print district_result

	return district_result




def helper_function_create_boundaries_sequential(district_result, district_min, max_number_of_bins, district_rounded_bin_amount,round_to_nearest,district_mean):

		next_boundary = district_min

		# Test printing 
		# print ""
		# print "district_min"
		# print district_min
		# print "district_mean"
		# print district_mean

		# print "district_rounded_bin_amount"
		# print district_rounded_bin_amount
		# print "next_boundary"
		# print next_boundary


		# initialize counter
		i = 0 
		while i < max_number_of_bins:

			# Test Printing
			# print  "In Loop: next_boundary: Before "
			# print next_boundary
	

			district_result[i] = {'percentile':next_boundary}
			next_boundary = round((next_boundary + district_rounded_bin_amount),round_to_nearest)

			# Test Printing
			# print  "In Loop: next_boundary: After "
			# print next_boundary
			
			i = i + 1 
		
		# # Test Printing 
		# print "district_result"
		# print district_result
		# print ""

		return district_result



def get_rounded_bin_boundary_percentiles_v2(field_of_interest,elementary_districts_infile,secondary_districts_infile,unified_districts_infile, \
	segment_districts,max_number_of_bins,max_bins_below_mean,max_bins_above_mean,straddle_mean,round_to_nearest,diverging_or_sequential,percent_or_not, \
	min_percentile,max_percentile):

	# Calculate Variables not influenced by any user options
	number_of_bins = max_number_of_bins
	elementary_result = {}
	secondary_result = {}
	unified_result = {}

	# Possibly Could delete this later
	# Calculate Basic stats for ENTIRE observations (all districts together)
	all_array = aggregate_3_district_infiles(field_of_interest,elementary_districts_infile,secondary_districts_infile,unified_districts_infile)
	all_max = find_max_2(all_array)
	all_min = find_min_2(all_array)
	all_range = all_max - all_min
	all_mean = find_mean_2(all_array)


	#################### Do Stuf related to Straddle or Not Stradle mean####################################
	
	if straddle_mean == "straddle_mean":
		numerator_for_initial_bins = 2.0  # if we straddle mean the the initial bins is half below the mean and half above (hence numerator of 2)
		pass
	elif straddle_mean == "do_not_straddle_mean":
		numerator_for_initial_bins = 1.0 # if we don't straddle mean the the initial bins (nearest mean) are whole bins  (hence numerator of 1)
		# if the mean is a boundary then we want 0 (i.e. the mean) as a stopp in boundary dictionary
		result_elementary_boundary = {0:{"percentile":0}}  
		result_secondary_boundary = {0:{"percentile":0}}
		result_unified_boundary = {0:{"percentile":0}}
		pass
	else: 
		print "error, set straddle mean to either 'straddle_mean' or 'do_not_straddle_mean'"
		return


	########## Do Stuff related to whether you segment_districts or not ################
	if segment_districts ==  "do_not_segment_districts":
		# Store array for each district - Elementary, Secondary, Then Unified
		elementary_array = aggregate_3_district_infiles(field_of_interest,elementary_districts_infile,secondary_districts_infile,unified_districts_infile)
		secondary_array = aggregate_3_district_infiles(field_of_interest,elementary_districts_infile,secondary_districts_infile,unified_districts_infile)
		unified_array = aggregate_3_district_infiles(field_of_interest,elementary_districts_infile,secondary_districts_infile,unified_districts_infile)
		pass
	elif segment_districts ==  "segment_districts":
		# Store array for each district - Elementary, Secondary, Then Unified
		elementary_array = open_and_store_in_array(field_of_interest,elementary_districts_infile)
		secondary_array = open_and_store_in_array(field_of_interest,secondary_districts_infile)
		unified_array = open_and_store_in_array(field_of_interest,unified_districts_infile)
		pass	
	else: 
		print "error, set 'segment_districts' to  either 'do_not_separate_districts' or 'separate_districts'"
		return

	# Do Caluculations Impacted by Segment or Not Segmened
	# Elementary
	elementary_max = find_max_2(elementary_array)
	elementary_min = find_min_2(elementary_array)
	elementary_range = elementary_max - elementary_min
	elementary_mean = find_mean_2(elementary_array)
	
	# Secondary	
	secondary_max = find_max_2(secondary_array)
	secondary_min = find_min_2(secondary_array)
	secondary_range = secondary_max - secondary_min
	secondary_mean = find_mean_2(secondary_array)
	# Unified
	unified_max = find_max_2(unified_array)
	unified_min = find_min_2(unified_array)
	unified_range = unified_max - unified_min
	unified_mean = find_mean_2(unified_array)

	# # Test Printing
	# print "elementary_max"
	# print elementary_max
	# print "elementary_min"
	# print elementary_min
	# print "elementary_range"
	# print elementary_range
	# print "elementary mean"
	# print elementary_mean
	print "Field of Interest = ", field_of_interest
	print "mean = ", all_mean



	#################### Do Stuf related to Percent  or Not Percent    ####################################

	if percent_or_not == "not_percent":
		# Set variables influenced by "percent_or_not" field:	
		#### Elementary ##########
		elementary_max_percentile = ((elementary_max / elementary_mean) - 1) * 100.0
		elementary_min_percentile = ((elementary_min / elementary_mean) - 1) * 100.0	
		elementary_range_percentile = elementary_max_percentile - elementary_min_percentile
		elementary_rounded_bin_amount = round((elementary_range_percentile/number_of_bins), round_to_nearest)
		elementary_left_of_mean = (-elementary_rounded_bin_amount/numerator_for_initial_bins) 
		elementary_right_of_mean = (elementary_rounded_bin_amount/numerator_for_initial_bins)
		#### Secondary  ##########
		secondary_max_percentile = ((secondary_max / secondary_mean) - 1) * 100.0
		secondary_min_percentile = ((secondary_min / secondary_mean) - 1) * 100.0	
		secondary_range_percentile = secondary_max_percentile - secondary_min_percentile
		secondary_rounded_bin_amount = round((secondary_range_percentile/number_of_bins), round_to_nearest)
		secondary_left_of_mean = (-secondary_rounded_bin_amount/numerator_for_initial_bins) 
		secondary_right_of_mean = (secondary_rounded_bin_amount/numerator_for_initial_bins)
		#### Unified ##########
		unified_max_percentile = ((unified_max / unified_mean) - 1) * 100.0
		unified_min_percentile = ((unified_min / unified_mean) - 1) * 100.0	
		unified_range_percentile = unified_max_percentile - unified_min_percentile
		unified_rounded_bin_amount = round((unified_range_percentile/number_of_bins), round_to_nearest)
		unified_left_of_mean = (-unified_rounded_bin_amount/numerator_for_initial_bins) 
		unified_right_of_mean = (unified_rounded_bin_amount/numerator_for_initial_bins)
		###### All Districts #############
		all_districts_min_array = [elementary_min,secondary_min,unified_min]
		all_districts_min = find_min_2(all_districts_min_array)
		all_districts_max_array = [elementary_max,secondary_max,unified_max]
		all_districts_max = find_max_2(all_districts_max_array)		

		#################### Do Stuf related whetehr a min and Max percentil is set ################################
		# Minimume First
		if min_percentile == None:
			all_districts_min_percentile_array = [elementary_min_percentile,secondary_min_percentile,unified_min_percentile]
			all_districts_min_percentile = find_min_2(all_districts_min_percentile_array)
			pass

		elif min_percentile != None:
			
			all_districts_min_percentile = min_percentile
		else:
			print "error, set 'Min Percentil to either 'None' or an integer"
			return

		# Maximum Next 
		if max_percentile == None:
			all_districts_max_percentile_array = [elementary_max_percentile,secondary_max_percentile,unified_max_percentile]
			all_districts_max_percentile = find_max_2(all_districts_max_percentile_array)
			pass
		elif max_percentile != None:
			all_districts_max_percentile = max_percentile
		else:
			print "error, set 'Max Percentil to either 'None' or an integer"
			return

		############## For NOT_PERCENT ONLY ...Do stuff that is dependent on Min and Max Percentile.....(i.e. All Districts) #############
		all_districts_range_percentile = all_districts_max_percentile - all_districts_min_percentile
		all_districts_rounded_bin_amount = round((all_districts_range_percentile/number_of_bins), round_to_nearest)
		all_districts_left_of_mean = -(all_districts_rounded_bin_amount/numerator_for_initial_bins) 
		all_districts_right_of_mean = (all_districts_rounded_bin_amount/numerator_for_initial_bins) 

		# Test Printing
		# print "percentile_min:elementary"
		# print elementary_min_percentile
		# print "percentile_min:secondary"
		# print secondary_min_percentile
		# print "percentile_min:unified"
		# print unified_min_percentile

		# print "percentile_max:elementary"
		# print elementary_max_percentile
		# print "percentile_max:secondary"
		# print secondary_max_percentile
		# print "percentile_max:unified"
		# print unified_max_percentile

		# # # Test Printing 
		# print "Not Percent"
		# print "elementary_max_percentile"
		# print elementary_max_percentile
		# print "elementary_min_percentile"
		# print elementary_min_percentile
		# print "elementary_range_percentile"
		# print elementary_range_percentile
		# print "elementary_rounded_bin_amount"
		# print elementary_rounded_bin_amount
		# print "elementary_left_of_mean"
		# print elementary_left_of_mean
		# print "elementary_right_of_mean"
		# print elementary_right_of_mean

		# print "all_districts_max_percentile"
		# print all_districts_max_percentile
		# print "all_districts_min_percentile"
		# print all_districts_min_percentile
		# print "all_district_range_percentile"
		# print all_districts_range_percentile
		# print "all_districts_rounded_bin_amount"
		# print all_districts_rounded_bin_amount
		# print "all_districts_left_of_mean"
		# print all_districts_left_of_mean
		# print "all_districts_right_of_mean"
		# print all_districts_right_of_mean


		pass

	elif percent_or_not == "percent":
		# Set variables influenced by "percent_or_not" field:	
		#### Elementary ##########
		elementary_max_percentile = elementary_max
		elementary_min_percentile = elementary_min
		elementary_range_percentile = elementary_max_percentile - elementary_min_percentile
		elementary_rounded_bin_amount = round((elementary_range / number_of_bins)*1.0, round_to_nearest)
		elementary_left_of_mean = elementary_mean - elementary_rounded_bin_amount
		elementary_right_of_mean = elementary_mean + elementary_rounded_bin_amount

		
		#### Secondary  ##########
		secondary_max_percentile = secondary_max
		secondary_min_percentile = secondary_min
		secondary_range_percentile = secondary_max_percentile - secondary_min_percentile
		secondary_rounded_bin_amount = round((secondary_range / number_of_bins)*1.0, round_to_nearest)
		secondary_left_of_mean = secondary_mean - secondary_rounded_bin_amount
		secondary_right_of_mean = secondary_mean + secondary_rounded_bin_amount
		#### Unified ##########
		unified_max_percentile = unified_max
		unified_min_percentile = unified_min
		unified_range_percentile = unified_max_percentile - unified_min_percentile
		unified_rounded_bin_amount = round((unified_range / number_of_bins)*1.0, round_to_nearest)
		unified_left_of_mean = unified_mean - unified_rounded_bin_amount
		unified_right_of_mean = unified_mean + unified_rounded_bin_amount
		####### All Districts#######
		all_districts_min_array = [elementary_min,secondary_min,unified_min]
		all_districts_min = find_min_2(all_districts_min_array)
		all_districts_max_array = [elementary_max,secondary_max,unified_max]
		all_districts_max = find_max_2(all_districts_max_array)
		
		#################### Do Stuf related whetehr a min and Max percentil is set ################################
		

		if min_percentile == None:
			all_districts_min_percentile = all_districts_min
			pass
		elif min_percentile != None:
			all_districts_min_percentile = min_percentile
			# print "all_districts_min_percentile"
			# print all_districts_min_percentile

		else:
			print "error, set 'Min Percentil to either 'None' or an integer"
			return

		# Maximum Next 
		if max_percentile == None:
			all_districts_max_percentile = all_districts_max
			pass
		elif max_percentile != None:
			all_districts_max_percentile = max_percentile
		else:
			print "error, set 'Max Percentil to either 'None' or an integer"
			return

		############## For PERCENT ONLY ...Do stuff that is dependent on Min and Max Percentile.....(i.e. All Districts) #############
		all_districts_range_percentile = all_districts_max_percentile - all_districts_min_percentile
		all_districts_rounded_bin_amount = round((all_districts_range_percentile/number_of_bins), round_to_nearest)
		all_districts_left_of_mean = int(all_mean)-(all_districts_rounded_bin_amount/numerator_for_initial_bins)    # This Formula differs for Percent vs no Percent 
		all_districts_right_of_mean = int(all_mean)+(all_districts_rounded_bin_amount/numerator_for_initial_bins) # This Formula differs for Percent vs no Percent 

		
		# # # Test Printing
		# print "all_districts_max_percentile"
		# print all_districts_max_percentile
		# print "all_districts_min_percentile"
		# print all_districts_min_percentile
		# print "all_district_range_percentile"
		# print all_district_range_percentile
		# print "all_districts_rounded_bin_amount"
		# print all_districts_rounded_bin_amount
		# print "all_districts_left_of_mean"
		# print all_districts_left_of_mean
		# print "all_districts_right_of_mean"
		# print all_districts_right_of_mean

		# # Test Printing
		# print  "Percent"
		# print "elementary_max_percentile"
		# print elementary_max_percentile
		# print "elementary_min_percentile"
		# print elementary_min_percentile
		# print "elementary_range_percentile"
		# print elementary_range_percentile
		# print "elementary_rounded_bin_amount"
		# print elementary_rounded_bin_amount
		# print "elementary_left_of_mean"
		# print elementary_left_of_mean
		# print "elementary_right_of_mean"
		# print elementary_right_of_mean


		pass
	else:
		print "Why did it make it here?"
		print "error, set 'percent_or_not' to 'percent' or 'not_percent'"
		return


	# print "all_mean"
	# print all_mean


	# print "all_districts_min_percentile"
	# print all_districts_min_percentile

	# print "all_districts_max_percentile"
	# print all_districts_max_percentile

	# print "all_districts_range_percentile"
	# print all_districts_range_percentile
	
	# print "number_of_bins"
	# print number_of_bins

	# print "all_districts_rounded_bin_amount"
	# print all_districts_rounded_bin_amount

	# print "numerator_for_initial_bins"
	# print numerator_for_initial_bins


	# print "all_districts_right_of_mean"
	# print all_districts_right_of_mean
	# print "all_districts_left_of_mean"
	# print all_districts_left_of_mean


	#################### Do Stuf related to Diverging or Sequential    ####################################
	
	if diverging_or_sequential == "diverging":
		
		elementary_result = helper_function_create_boundaries_diverging(elementary_result, \
			all_districts_left_of_mean,all_districts_right_of_mean, \
			all_districts_min_percentile,all_districts_max_percentile,all_mean,\
			max_bins_below_mean,max_bins_above_mean, \
			all_districts_rounded_bin_amount,round_to_nearest, percent_or_not)

		secondary_result = helper_function_create_boundaries_diverging(secondary_result, \
			all_districts_left_of_mean,all_districts_right_of_mean, \
			all_districts_min_percentile,all_districts_max_percentile,all_mean,\
			max_bins_below_mean,max_bins_above_mean, \
			all_districts_rounded_bin_amount,round_to_nearest, percent_or_not)


		unified_result = helper_function_create_boundaries_diverging(unified_result, \
			all_districts_left_of_mean,all_districts_right_of_mean, \
			all_districts_min_percentile,all_districts_max_percentile,all_mean,\
			max_bins_below_mean,max_bins_above_mean, \
			all_districts_rounded_bin_amount,round_to_nearest, percent_or_not)


	elif diverging_or_sequential == "sequential":

		elementary_result = helper_function_create_boundaries_sequential(elementary_result, all_districts_min_percentile, max_number_of_bins, all_districts_rounded_bin_amount,round_to_nearest,all_mean)
		secondary_result = helper_function_create_boundaries_sequential(secondary_result, all_districts_min_percentile, max_number_of_bins, all_districts_rounded_bin_amount,round_to_nearest,all_mean)
		unified_result = helper_function_create_boundaries_sequential(unified_result, all_districts_min_percentile, max_number_of_bins, all_districts_rounded_bin_amount,round_to_nearest,all_mean)

		pass
	else:
		print "error, either choose 'diverging' or 'sequential'" 
		return

	# # Test Printing 
	print ""
	print " Field of Interest"
	print field_of_interest
	print "elementary_result"
	print elementary_result
	print "secondary_result"
	print secondary_result
	print "unified_result"
	print unified_result
	print ""

	return 	elementary_result, secondary_result, unified_result



# Function that find the Stops of a field.  Find it by taking rounded percentile number and multiplying by mean of given field 
def find_boundary_based_on_mean_and_percentiles_array(mean, percentile_boundary_array):
	result = []
	for each in percentile_boundary_array:
		index =  (1+(each/100.0))
		value_to_store = index * mean
		result.append(int(value_to_store))
	# print result 	 
	return result

# Function that adds in the numberical stops  to a dictionary storing all the bin information on given field. 
# The stops are added in so the javascript knows exactly where to stop and go to next color for a given bin. 
def add_stops_to_dictonary(field_of_interest,elementary_districts_infile,secondary_districts_infile,unified_districts_infile, \
	segment_districts,max_number_of_bins,max_bins_below_mean,max_bins_above_mean,\
	straddle_mean,round_to_nearest,diverging_or_sequential,percent_or_not,min_percentile,max_percentile):
	elementary_boundary_dictionary,secondary_boundary_dictionary,unified_boundary_dictionary = get_rounded_bin_boundary_percentiles_v2( \
		field_of_interest, 
		elementary_districts_infile,
		secondary_districts_infile,
		unified_districts_infile,
		segment_districts,
		max_number_of_bins,
		max_bins_below_mean,
		max_bins_above_mean,
		straddle_mean,
		round_to_nearest,
		diverging_or_sequential,
		percent_or_not,
		min_percentile,
		max_percentile)

	# initialize Percentile Arrays from boundary dictionaries and store 
	elementary_percentile_array = []
	secondary_percentile_array = []
	unified_percentile_array = []

	for index, value in elementary_boundary_dictionary.items():
		elementary_percentile_array.append(value["percentile"])
	for index, value in secondary_boundary_dictionary.items():
		secondary_percentile_array.append(value["percentile"])
	for index, value in unified_boundary_dictionary.items():
		unified_percentile_array.append(value["percentile"])

	
	############## Do Stuff related to whether Segment District or Do NOT segment Districts ################
	# Finding Means
	if segment_districts == "segment_districts":
		elementary_mean_value = find_mean(elementary_districts_infile,field_of_interest)
		secondary_mean_value = find_mean(secondary_districts_infile,field_of_interest)
		unified_mean_value = find_mean(unified_districts_infile,field_of_interest)
		pass

	elif segment_districts == "do_not_segment_districts":
		aggregate_array = aggregate_3_district_infiles(field_of_interest,elementary_districts_infile,secondary_districts_infile,unified_districts_infile)
		aggregate_mean_value = find_mean_2(aggregate_array)
		elementary_mean_value = aggregate_mean_value
		secondary_mean_value = aggregate_mean_value
		unified_mean_value = aggregate_mean_value
		pass

	else:
		print "Error choose 'do_not_segment_districts' or 'segment_districts' for segment districts,"
		return


	############## Do Stuff related to Percent or Not Percent ################################################
	if percent_or_not == "not_percent":
		for index, value in elementary_boundary_dictionary.items():
			percentile = (value["percentile"]/100.0) 		#Make sure to use .0 so doesn't turnn into integer
			value["stop"] = int((elementary_mean_value * (1+percentile)))

		for index, value in secondary_boundary_dictionary.items():
			percentile = (value["percentile"]/100.0) 		#Make sure to use .0 so doesn't turnn into integer
			value["stop"] = int((secondary_mean_value * (1+percentile)))	

		for index, value in unified_boundary_dictionary.items():
			percentile = (value["percentile"]/100.0) 		#Make sure to use .0 so doesn't turnn into integer
			value["stop"] = int((unified_mean_value * (1+percentile)))		
		pass
			
	elif percent_or_not == "percent":
		if diverging_or_sequential == "diverging":
			for index, value in elementary_boundary_dictionary.items():
				percentile = value["percentile"] 		#Make sure to use .0 so doesn't turnn into integer
				value["stop"] = (int(elementary_mean_value) + percentile)

			for index, value in secondary_boundary_dictionary.items():
				percentile = value["percentile"] 		#Make sure to use .0 so doesn't turnn into integer
				value["stop"] = (int(secondary_mean_value) + percentile)


			for index, value in unified_boundary_dictionary.items():
				percentile = value["percentile"] 		#Make sure to use .0 so doesn't turnn into integer
				value["stop"] = (int(unified_mean_value) + percentile)
			pass
		elif diverging_or_sequential == "sequential":
			for index, value in elementary_boundary_dictionary.items():
				percentile = value["percentile"] 		#Make sure to use .0 so doesn't turnn into integer
				value["stop"] = percentile

			for index, value in secondary_boundary_dictionary.items():
				percentile = value["percentile"] 		#Make sure to use .0 so doesn't turnn into integer
				value["stop"] = percentile


			for index, value in unified_boundary_dictionary.items():
				percentile = value["percentile"] 		#Make sure to use .0 so doesn't turnn into integer
				value["stop"] = percentile
			pass


		else:
			print "Error, choose either 'sequential' or 'divergin' for field 'diverging_or_sequential'"
			return 
	
	else: 
		print "Error, choose either 'percent' or 'not_percent' for field 'percent_or_not'"
		return 
	

	# # Test Printing 
	print ""
	print "Field of Interest"
	print field_of_interest
	print "elementary_boundary_dictionary"
	print elementary_boundary_dictionary
	print "secondary_boundary_dictionary"
	print secondary_boundary_dictionary
	print "unified_boundary_dictionary"
	print unified_boundary_dictionary
	print ""

	return elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary
	

############ Define Color Dictionary ################ 
# THe two dictionaries below store the information for color dictionaries 
# they can be changed if you desire a differently color pallette,  
# Note - When using function like (e.g. get_rounded_bin_boundary_percentiles) the number of colors must match up with the Maximum bins allowed field in some of the other functions 
# Note2 - Abandoned idea of inputing 2 (or 3) colors and creating steps programmatically.  See python sript "06_EdViz_Color_Picking.py" or "06_EdViz_Color_Picking_HSL.py". Instead going with a manual method  ################ 

diverging_color_dictionary = {0:"#f7f7f7",1:"#d9f0d3",2:"#a6dba0",3:"#5aae61",4:"#1b7837",5:"#00441b",-1:"#e7d4e8",-2:"#c2a5cf",-3:"#9970ab",-4:"#762a83",-5:"#40004b"}
sequential_color_dictionary = {0:"#fff5eb",1:"#fee6ce",2:"#fdd0a2",3:"#fdae6b",4:"#fd8d3c",5:"#f16913",6:"#d94801",7:"#a63603",8:"#7f2704",9:"#681f02"}

# Create a function for updating boundary dictionary with color
def update_boundary_dictionary_with_color(boundary_dictionary,color_dictionary):
	for key, value in boundary_dictionary.iteritems():
		value["color"] =  color_dictionary[key]
	return boundary_dictionary


# Join color and stops together (also uses function above)
def join_colors_and_stops(field_of_interest,elementary_infile,secondary_districts_infile,unified_districts_infile, \
	segment_districts,max_number_of_bins,max_bins_below_mean,max_bins_above_mean,\
	straddle_mean,round_to_nearest,diverging_or_sequential,color_dictionary,percent_or_not, min_percentile,max_percentile):
	
	# Run the script that adds stops to dictionary
	elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary = add_stops_to_dictonary(field_of_interest, \
		elementary_infile,secondary_districts_infile,unified_districts_infile, \
		segment_districts,max_number_of_bins,max_bins_below_mean,max_bins_above_mean,\
		straddle_mean,round_to_nearest,diverging_or_sequential,percent_or_not,min_percentile,max_percentile)


	# Add color to the boundary dictionary
	updated_elementary_boundary_dictionary = update_boundary_dictionary_with_color(elementary_boundary_dictionary,color_dictionary)
	updated_secondary_boundary_dictionary  = update_boundary_dictionary_with_color(secondary_boundary_dictionary,color_dictionary)
	updated_unified_boundary_dictionary = update_boundary_dictionary_with_color(unified_boundary_dictionary,color_dictionary)
	
	return updated_elementary_boundary_dictionary,updated_secondary_boundary_dictionary, updated_unified_boundary_dictionary


# A function that takes an array of field names and creates a single legends dictionary (for each district).  This legends dictionary will get added into the final GEOJSON file  
def add_multiple_fields_to_legend_dictionary_and_write_to_file(field_names_array,elementary_boundary_dictionary,secondary_boundary_dictionary,unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,year):
	
	for field in field_names_array:
		
		if field in elementary_boundary_dictionary:
			elementary_legends_dictionary[field] = elementary_boundary_dictionary[field]
		else:
			pass
		
		if field in secondary_boundary_dictionary:
			secondary_legends_dictionary[field] = secondary_boundary_dictionary[field]
		else:
			pass

		if field in unified_boundary_dictionary:
			unified_legends_dictionary[field] = unified_boundary_dictionary[field]
		else:
			pass	

	
	outfile_path_elementary = "..\\output\\"+year+"_elementary_"+"legends_dictionary_only.py"
	outfile_path_secondary = "..\\output\\"+year+"_secondary_"+"legends_dictionary_only.py"
	outfile_path_unified = "..\\output\\"+year+"_unified_"+"legends_dictionary_only.py"

	with open(outfile_path_elementary, 'w') as outfile:
	    geojson.dump(elementary_legends_dictionary, outfile)

	with open(outfile_path_secondary, 'w') as outfile:
		    geojson.dump(secondary_legends_dictionary, outfile)
	with open(outfile_path_unified, 'w') as outfile:
		    geojson.dump(unified_legends_dictionary, outfile)

	return 



def read_legend_dictionary_from_file(year,district_type):

	# Crate infile path
	infile_path = "..\\output\\"+year+"_"+district_type+"_legends_dictionary_only.py"

	# oPEN Infile and store as legend dictionary
	with open(infile_path) as f:
		legends_dictionary = geojson.load(f)

	return legends_dictionary




def update_geojson_with_legends_dictionary(legends_dictionary,geojson_file,year,district_type):
	# Crate infile path
	infile_path = "..\\output\\"+year+"_"+district_type+".geojson"

	# Open Files
	with open(infile_path) as f:
		districts = geojson.load(f)

	districts["legends"] = legends_dictionary

	# store out file locations
	outfile_path = "..\\output\\"+year+"_"+district_type+"_with_legends.geojson"
	

	# Write the file to disk
	with open(outfile_path, 'w') as outfile:
	     geojson.dump(districts, outfile)

	return


def javascript_output(boundary_dictionary):
	result = []

	# iterate through boundary dictionary and append both stops and color to result array
	print "This is Javascript printed output "
	for field, boundary_sub_dictionary in boundary_dictionary.iteritems():
		print field
		for key, value in boundary_sub_dictionary.iteritems():
			result.append([value['stop'],value['color']])
			# sort the result with smaller stops first
			result.sort(key=lambda x:x[0])
		print result 
		result = []

	return " "


"""Run Summary Scripts for fields that apply to all 3 district types"""
# run_summary_script_all_districts("IEPP_2015",elementary_districts_infile,secondary_districts_infile,unified_districts_infile)
# run_summary_script_all_districts("OEPP_2015",elementary_districts_infile,secondary_districts_infile,unified_districts_infile)
# run_summary_script_all_districts("Instruction_Percent_2015",elementary_districts_infile,secondary_districts_infile,unified_districts_infile)
# run_summary_script_all_districts("Ave_Teacher_Salary_2015",elementary_districts_infile,secondary_districts_infile,unified_districts_infile)
# run_summary_script_all_districts("Teacher_Rentention_Rate_2015",elementary_districts_infile,secondary_districts_infile,unified_districts_infile)
# run_summary_script_all_districts("Low_Income_Percent_2015",elementary_districts_infile,secondary_districts_infile,unified_districts_infile)
# run_summary_script_all_districts("District_White_Percent_2015",elementary_districts_infile,secondary_districts_infile,unified_districts_infile)
# run_summary_script_all_districts("District_Black_Percent_2015",elementary_districts_infile,secondary_districts_infile,unified_districts_infile)
# run_summary_script_all_districts("District_Hispanic_Percent_2015",elementary_districts_infile,secondary_districts_infile,unified_districts_infile)
# run_summary_script_all_districts("District_Asian_Percent_2015",elementary_districts_infile,secondary_districts_infile,unified_districts_infile)
# run_summary_script_all_districts("Composite_Percent_Meets_or_Exceeds_Read_and_Math_2014",elementary_districts_infile,secondary_districts_infile,unified_districts_infile)

# run_summary_script_all_districts("Homeless_Percent_2015",elementary_districts_infile,secondary_districts_infile,unified_districts_infile)




"""Run summary scripts for fields that apply to Highschool only....i.e. Secondary districts AND unified"""
# run_summary_script_secondary_and_unified("HS_4_Year_Graduation_Rate_Percent_2015",secondary_districts_infile,unified_districts_infile)
# run_summary_script_secondary_and_unified("HS_5_Year_Graduation_Rate_Percent_2015",secondary_districts_infile,unified_districts_infile)
# run_summary_script_secondary_and_unified("ACT_Comp_2015",secondary_districts_infile,unified_districts_infile)
# run_summary_script_secondary_and_unified("Percent_Ready_For_College_2015",secondary_districts_infile,unified_districts_infile)
# print "IEPP_2015"
# print "Elementary  = ", find_boundaries_percentiles_mean_only(6508,[-.5,-.25,0,.25,.50,.75,1,1.25])
# print "Secondary  = ", find_boundaries_percentiles_mean_only(8544,[-.5,-.25,0,.25,.50,.75,1,1.25])
# print "Unified = ", find_boundaries_percentiles_mean_only(5791,[-.5,-.25,0,.25,.50,.75,1,1.25])
# print "OEPP_2015"
# print "Elementary  = ", find_boundaries_percentiles_mean_only(11440,[-.5,-.25,0,.25,.50,.75,1,1.25])
# print "Secondary  = ", find_boundaries_percentiles_mean_only(15089,[-.5,-.25,0,.25,.50,.75,1,1.25])
# print "Unified = ", find_boundaries_percentiles_mean_only(10181,[-.5,-.25,0,.25,.50,.75,1,1.25])
# print "Instruction_Percent_2015"
# print "State Average   = ", find_boundaries_percentiles_mean_only(47,[-.3,-.2,-.1,0,.1,.2,.3,.4])
# print "HS_4_Year_Graduation_Rate_Percent_2015"
# print "State Average   = ", find_boundaries_percentiles_mean_only(86,[-.3,-.2,-.1,0,.1,.2,.3,.4])
# print "HS_5_Year_Graduation_Rate_Percent_2015"
# print "State Average   = ", find_boundaries_percentiles_mean_only(88,[-.3,-.2,-.1,0,.1,.2,.3,.4])
# print "HS_5_Year_Graduation_Rate_Percent_2015"
# print "State Average   = ", find_boundaries_percentiles_mean_only(88,[-.3,-.2,-.1,0,.1,.2,.3,.4])
# print "ACT_Comp_2015"
# print "State Average   = ", find_boundaries_percentiles_mean_only(20,[-.3,-.2,-.1,0,.1,.2,.3,.4])
# print "Percent Ready for College"
# print "State Average   = ", find_boundaries_percentiles_mean_only(42.5,[-.3,-.2,-.1,0,.1,.2,.3,.4])
# print "Meets or exceed Reading and Matth"
# print "State Average   = ", find_boundaries_percentiles_mean_only(59,[-.3,-.2,-.1,0,.1,.2,.3,.4])


"""Run describe and histogram scripts"""
#IEPP
# Elementry 
# array = open_and_store_in_array("IEPP_2015",elementary_districts_infile)
# print describe_and_run_histogram_equal_bin_size_around_mean(array,11,5,5,1,"Instructional Expenditure Per Pupil 2015")
# Secondary
# array = open_and_store_in_array("IEPP_2015",secondary_districts_infile)
# print describe_and_run_histogram_equal_bin_size_around_mean(array,22,15,15,1,"Instructional Expenditure Per Pupil 2015")
# Unified
# array = open_and_store_in_array("IEPP_2015",unified_districts_infile)
# print describe_and_run_histogram_equal_bin_size_around_mean(array,11,5,5,1,"Instructional Expenditure Per Pupil 2015")


# # Local_Property_Tax_Percent_2015
# # # Unified
# array = open_and_store_in_array("Local_Property_Tax_Percent_2015",unified_districts_infile)
# print describe_and_run_histogram_equal_bin_size_around_mean(array,11,5,5,1,"Unified: Local Property Tax Percent 2015")

# Instruction_Percent_2015
# Unified 
# array = open_and_store_in_array("Instruction_Percent_2015",unified_districts_infile)
# print describe_and_run_histogram_equal_bin_size_around_mean(array,11,5,5,1,"Unified: Local Property Tax Percent 2015")
# # Aggregate 
# array = aggregate_3_district_infiles("Instruction_Percent_2015",elementary_districts_infile,secondary_districts_infile,unified_districts_infile)
# print describe_and_run_histogram_equal_bin_size_around_mean(array,11,5,5,1,"Instruction Percent 2015")


#"Homeless"
# # Aggregate 
# array = aggregate_3_district_infiles("Homeless_Percent_2015",elementary_districts_infile,secondary_districts_infile,unified_districts_infile)
# print describe_and_run_histogram_equal_bin_size_around_mean(array,11,5,5,1,"Homeless  Percent 2015")

# # "HS_4_Year_Graduation_Rate_Percent_2015"
# array = open_and_store_in_array("HS_4_Year_Graduation_Rate_Percent_2015",unified_districts_infile)
# print describe_and_run_histogram_equal_bin_size_around_mean(array,11,5,5,1,"HS_4_Year_Graduation_Rate_Percent_2015")


# # "EAV_Per_Pupil_2015"
# array = open_and_store_in_array("EAV_Per_Pupil_2015",unified_districts_infile)
# print describe_and_run_histogram_equal_bin_size_around_mean(array,11,5,5,1,"EAV_Per_Pupil_2015")


# Problem with this one 

# # Total_School_Tax_Rate_Per_100_Dollars_2015
# array = open_and_store_in_array("Total_School_Tax_Rate_Per_100_Dollars_2015",unified_districts_infile)
# print array
# # print describe_and_run_histogram_equal_bin_size_around_mean(array,11,5,5,1,"Total_School_Tax_Rate_Per_100_Dollars_2015")


# # Bach_Degree_2015

# # # Unified
# array = open_and_store_in_array("Bach_Degree_2015",unified_districts_infile)
# print describe_and_run_histogram_equal_bin_size_around_mean(array,11,5,5,1,"Unified: Bach_Degree_2015")

# Race =  All 3 districts  
# Note - used this for CAT Presentation on data visualization 
# array = aggregate_3_district_infiles("District_Asian_Percent_2015",elementary_districts_infile,secondary_districts_infile,unified_districts_infile)
# print describe_and_run_histogram_equal_bin_size_around_mean(array,13,15,15,1,"Percentage of Asian Students ")
# array = aggregate_3_district_infiles("District_Black_Percent_2015",elementary_districts_infile,secondary_districts_infile,unified_districts_infile)
# print describe_and_run_histogram_equal_bin_size_around_mean(array,20,10,10,1,"Percentage of Black Students ")
# array = aggregate_3_district_infiles("District_Hispanic_Percent_2015",elementary_districts_infile,secondary_districts_infile,unified_districts_infile)
# print describe_and_run_histogram_equal_bin_size_around_mean(array,20,10,10,1,"Percentage of Hispanic Students ")
# array = aggregate_3_district_infiles("District_White_Percent_2015",elementary_districts_infile,secondary_districts_infile,unified_districts_infile)
# print describe_and_run_histogram_equal_bin_size_around_mean(array,20,10,10,1,"Percentage of White Students ")
# array = aggregate_3_district_infiles("District_Asian_Percent_2015",elementary_districts_infile,secondary_districts_infile,unified_districts_infile)
# print describe_and_run_histogram_equal_bin_size_around_mean(array,20,10,10,1,"Percentage of Asian Students ")
			# !!!!!!!!!!!!!Can't get Asian histogram to function!!





#####################################  - Create a Legends dictionary that will get appended to GEOJSON #################################################
# Note - For multiple fields at once
# Note - If there isn't a boundary dictionary then legend dictionary won't be made.  Make sure to manually create bound

# Stores the names of QUANTITATIVE fields that require a legend.  Note,..not all fields..just quantiative

quantitative_col_titles_2016 = {
	# Student Data: Race
	29:'District_White_Percent_2016',
	30:'District_Black_Percent_2016',
	31:'District_Hispanic_Percent_2016',
	32:'District_Asian_Percent_2016',
	33:'District_Native_Hawaiian_or_Pac_Islander_Percent_2016',
	34:'District_Native_American_Percent_2016',
	35:'District_Two_or_More_Races_Percent_2016',
	# Student Data: Disabilities	
	47:'LEP_Percent_2016',
	51:'IEP_Percent_2016',
	# Student Data: other
	55:'Low_Income_Percent_2016',
	59:'Homeless_Percent_2016',
	# Student Data: Performance
	143:'HS_4_Year_Grad_Rate_2016',
	199:'HS_5_Year_Grad_Rate_2016',
	255:'HS_6_Year_Grad_Rate_2016',		# NEw Field 
	311:'HS_7_Year_Grad_Rate_2016',		# NEw Field 
	# Student Data: ACT Related
	367:'ACT_Comp_2016',								
	387:'Percent_Ready_For_College_2016',
	391:'Percent_Student_Met_English_Benchmark_2016',
	395:'Percent_Student_Met_Math_Benchmark_2016',
	399:'Percent_Student_Met_Read_Benchmark_2016',
	403:'Percent_Student_Met_Sci_Benchmark_2016',
	407:'Percent_Student_Met_All_4_Benchmark_2016',

	# Teacher States 
	451:'Ave_Class_Size_2016',
	523:'Ave_Teacher_Exp_2016',
	531:'Bach_Degree_2016',
	539:'Masters_Plus_Degree_2016',
	547:'Pupil_Teacher_Ratio_Elem_2016',
	551:'Pupil_Teacher_Ratio_HS_2016',
	563:'Ave_Teacher_Salary_2016',
	567:'Ave_Admin_Salary_2016',
	573:'Teacher_Rentention_Rate_2016',
	
	# THese 5 total to 100%
	580:'Local_Property_Tax_Percent_2016',
	583:'Other_Local_Funding_Percent_2016',
	586:'General_State_Aid_Percent_2016',
	589:'Other_State_Funding_Percent_2016',
	592:'Federal_Funding_Percent_2016',
	594:'Total_Revenue_Source_2016',

	# OTher School Finance Stuff
	595:'EAV_Per_Pupil_2016',
	598:'School_Tax_Rate_Per_100_Dollars_2016',
	601:'IEPP_2016',
	605:'OEPP_2016',

	# Theses 4 are a general category (totals to 100%) 
	610:'Instruction_Percent_2016',
	613:'General_Admin_Percent_2016',
	616:'Support_Services_Percent_2016',
	619:'Other_Expenditures_Percent_2016',

	# Theses 8 are a the detailed version (totals to 100%) 
	
	622:'Education_Percent_2016',
	625:'Operations_Percent_2016',
	628:'Transportation_Percent_2016',
	631:'Debt_Service_Percent_2016',
	634:'Tort_Fund_Percent_2016',
	637:'Munic_Retirement_And_Soc_Sec_Percent_2016',
	640:'Fire_Prevention_And_Safety_Percent_2016',
	643:'Capital_Projects_2016',
	645:'Total_Expenditures_2016',


	################ Problems with these ######################



	################# Skipping These ##########################
	36:'District_Total_Enrollment_2016', 
	63:'Total_School_Days_2016',
	67:'Parental_Invovlment_Percent_2016',
	139:'Dropout_Rate_Percent_2016',  # Dropout rate is not what it sounds like ...refers to students moving out of a district
	}

quantitative_col_titles_2015 = {
	########## Primary Focus Data ##############
	# Student Data: Race
	29:'District_White_Percent_2015',
	30:'District_Black_Percent_2015',
	31:'District_Hispanic_Percent_2015',
	32:'District_Asian_Percent_2015',
	33:'District_Native_Hawaiian_or_Pac_Islander_Percent_2015',
	34:'District_Native_American_Percent_2015',
	35:'District_Two_or_More_Races_Percent_2015',
	# Student Data: Disabilities	
	47:'LEP_Percent_2015',
	51:'IEP_Percent_2015',
	# Student Data: other
	55:'Low_Income_Percent_2015',
	59:'Homeless_Percent_2015',
	# Student Data: Performance
	143:'HS_4_Year_Grad_Rate_2015',
	199:'HS_5_Year_Grad_Rate_2015',
	# Student Data: ACT Related
	255:'ACT_Comp_2015',
	275:'Percent_Ready_For_College_2015',
	279:'Percent_Student_Met_English_Benchmark_2015',
	283:'Percent_Student_Met_Math_Benchmark_2015',
	287:'Percent_Student_Met_Read_Benchmark_2015',
	291:'Percent_Student_Met_Sci_Benchmark_2015',
	295:'Percent_Student_Met_All_4_Benchmark_2015',
	# Teacher States 
	339:'Ave_Class_Size_2015',
	411:'Ave_Teacher_Exp_2015',  ########### Problem ######### No values in this field?
	419:'Bach_Degree_2015',
	427:'Masters_Plus_Degree_2015',
	435:'Pupil_Teacher_Ratio_Elem_2015',
	439:'Pupil_Teacher_Ratio_HS_2015',
	451:'Ave_Teacher_Salary_2015',
	455:'Ave_Admin_Salary_2015',
	469:'Percent_Class_Not_Taught_By_High_Qual_Teacher_2015',
	477:'Teacher_Rentention_Rate_2015',
	# THese 5 total to 100%
	484:'Local_Property_Tax_Percent_2015',
	487:'Other_Local_Funding_Percent_2015',
	490:'General_State_Aid_Percent_2015',
	493:'Other_State_Funding_Percent_2015',
	496:'Federal_Funding_Percent_2015',
	# OTher School Finance Stuff
	499:'EAV_Per_Pupil_2015',									
	502:'School_Tax_Rate_Per_100_Dollars_2015',			
	505:'IEPP_2015',											
	509:'OEPP_2015',											
	# Theses 4 are a general category (totals to 100%) 
	514:'Instruction_Percent_2015',
	517:'General_Admin_Percent_2015',
	520:'Support_Services_Percent_2015',
	523:'Other_Expenditures_Percent_2015',
	# Theses 8 are a the detailed version (totals to 100%) 
	526:'Education_Percent_2015',
	529:'Operations_Percent_2015',
	532:'Transportation_Percent_2015',
	535:'Debt_Service_Percent_2015',
	538:'Tort_Fund_Percent_2015',
	541:'Munic_Retirement_And_Soc_Sec_Percent_2015',
	544:'Fire_Prevention_And_Safety_Percent_2015',
	547:'Capital_Projects_2015',

	########## Skipping these ####################
	36:'District_Total_Enrollment_2015', 
	63:'Total_School_Days_2015',
	67:'Parental_Invovlment_Percent_2015',
	139:'Dropout_Rate_Percent_2015',  				# Refers to students moving out of a district
	498:'Total_Revenue_Source_2015',
	549:'Total_Expenditures_2015'
	}
	
		
# quantitative_col_titles_2014 = {
# 	# Not displaying for simplicity
# 	505:'IEPP_2014',
# 	509:'OEPP_2014',												
# 	# Problems
# 	896: 'Meets_or_Exceeds_Read_and_Math_2014',
# 	9328:'Percent_College_within_16_months_2014',
# 	9332:'Percent_College_within_12_months_2014',
# 	9336:'Percent_Freshmen_On_Track_2014'
# 	}


##### Store the names of all Column Titles used 2014 and 2015
quantitative_col_titles_all = []



for key, value in quantitative_col_titles_2016.items():    	# Cycle throught 2016 column titles
	quantitative_col_titles_all.append(value)					# Append to array


for key, value in quantitative_col_titles_2015.items():    	# Cycle throught 2015 column titles
	quantitative_col_titles_all.append(value)					# Append to array

# for key, value in quantitative_col_titles_2014.items():		# Cycle through 2014 column title
# 	quantitative_col_titles_all.append(value)					# Append it to array

## Test Print it!	
# print quantitative_col_titles_all






######### Initialize Boundary Dictionaries
# Do this once for final run through....or if testing thing you may need these uncommented 
## Keep this one Uncommented 
# elementary_boundary_dictionary = {}
# secondary_boundary_dictionary = {}
# unified_boundary_dictionary = {}

# # Do this one only for first run....or if testing...but not when doing all other run throughs
# elementary_legends_dictionary  = {}
# secondary_legends_dictionary  = {}
# unified_legends_dictionary  = {}



############  Beg = Storing first field  into legends dictionary  ##################

# !!!!!!!!!!!!!!!!!        WARNING  !!!!!!!!!!!!!!!!!!!!  
# !!!!!!!!! If starting from scrath...make sure to delete the existing file!!!!!!!!!! 


# As if it exists the function will only ADD additional fields....won't clear out old ones 
#(this is by design so that later you can add fields without rewriting entire file)


# ###### Race
# ### 2015 
# large_race_field_name_array_2015 = ['District_White_Percent_2015','District_Black_Percent_2015', 'District_Hispanic_Percent_2015']
# for field in large_race_field_name_array_2015:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",10,5,5,"straddle_mean",0, \
# 		"sequential",sequential_color_dictionary,"percent",0,100)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(large_race_field_name_array_2015,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")
# ### 2016
# large_race_field_name_array_2016 = ['District_White_Percent_2016','District_Black_Percent_2016', 'District_Hispanic_Percent_2016']
# for field in large_race_field_name_array_2016:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",10,5,5,"straddle_mean",0, \
# 		"sequential",sequential_color_dictionary,"percent",0,100)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(large_race_field_name_array_2016,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")


# # ############  End = Storing data into First Fields   ##################






############## Beg = Store all field after initial set ####################################

# # # Initialize a Boundary dictionary (do this once) for each of the group below
# elementary_boundary_dictionary = {}
# secondary_boundary_dictionary = {}
# unified_boundary_dictionary = {}


# # # # # Read the legneds dictionary into file (do this once) for each of the group below

# elementary_legends_dictionary  = read_legend_dictionary_from_file("2017","elementary")
# secondary_legends_dictionary  = read_legend_dictionary_from_file("2017","secondary")
# unified_legends_dictionary  = read_legend_dictionary_from_file("2017","unified")
																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																												


############### Begin repeating for all group AFTER initial group ##################
### Group 0   .... store Races requiring rounding of 10
### 2015 
# asian_array_2015 = ['District_Asian_Percent_2015']
# for field in asian_array_2015:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",10,5,5,"straddle_mean",0, \
# 		"sequential",sequential_color_dictionary,"percent",0,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(asian_array_2015,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary, \
# 	elementary_legends_dictionary, secondary_legends_dictionary,unified_legends_dictionary,"2017")
# ### 2016
# asian_array_2016 = ['District_Asian_Percent_2016']
# for field in asian_array_2016:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",10,5,5,"straddle_mean",0, \
# 		"sequential",sequential_color_dictionary,"percent",0,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(asian_array_2016,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary, \
# 	elementary_legends_dictionary, secondary_legends_dictionary,unified_legends_dictionary,"2017")


######### Group 1 
### StoreRaces requiring rounding of 1
# ### 2015 
# small_race_field_name_array_2015 = ['District_Two_or_More_Races_Percent_2015']
# for field in small_race_field_name_array_2015:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",10,5,5,"straddle_mean",0,\
# 		"sequential",sequential_color_dictionary,"percent",0,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(small_race_field_name_array_2015,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")
# ### 2016
# small_race_field_name_array_2016 = ['District_Two_or_More_Races_Percent_2016']
# for field in small_race_field_name_array_2016:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",10,5,5,"straddle_mean",0,\
# 		"sequential",sequential_color_dictionary,"percent",0,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(small_race_field_name_array_2016,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")


####### Group 2
##  Races requiring rounding of 0.1
### 2015
# very_small_race_field_name_array_2015 = ['District_Native_Hawaiian_or_Pac_Islander_Percent_2015', 'District_Native_American_Percent_2015']
# # Update the boundary dictionary with colors and stops of new fields 
# for field in very_small_race_field_name_array_2015:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",10,5,5,"straddle_mean",1, \
# 		"sequential",sequential_color_dictionary,"percent",0,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(very_small_race_field_name_array_2015,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")
# ## 2016
# very_small_race_field_name_array_2016 = ['District_Native_Hawaiian_or_Pac_Islander_Percent_2016', 'District_Native_American_Percent_2016']
# for field in very_small_race_field_name_array_2016:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",10,5,5,"straddle_mean",1, \
# 		"sequential",sequential_color_dictionary,"percent",0,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(very_small_race_field_name_array_2016,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")


####### Group 3
## Large Numbers, diverging scale, Segment the Districts
## 2015
# large_number_array_separate_2015  = ["IEPP_2015","OEPP_2015"]
# for field in large_number_array_separate_2015:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"segment_districts",11,5,5,"do_not_straddle_mean",-1, \
# 		"diverging",diverging_color_dictionary,"not_percent",-100,100)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(large_number_array_separate_2015,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")
# ## 2016
# large_number_array_separate_2016  = ["IEPP_2016","OEPP_2016"]
# for field in large_number_array_separate_2016:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"segment_districts",11,5,5,"do_not_straddle_mean",-1, \
# 		"diverging",diverging_color_dictionary,"not_percent",-100,100)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(large_number_array_separate_2016,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")




# ###### Group 4 
# #Large Numbers, diverging scale, Do NOT SEPARATE the Districts
## 2015
# large_number_array_do_not_separate_2015 = ["Ave_Teacher_Salary_2015"]
# for field in large_number_array_do_not_separate_2015:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",11,5,5,"straddle_mean",-1, \
# 		"diverging",diverging_color_dictionary,"not_percent",-100,100)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(large_number_array_do_not_separate_2015,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")
# ## 2016
# large_number_array_do_not_separate_2016 = ["Ave_Teacher_Salary_2016"]
# for field in large_number_array_do_not_separate_2016:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",11,5,5,"straddle_mean",-1, \
# 		"diverging",diverging_color_dictionary,"not_percent",-100,100)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(large_number_array_do_not_separate_2016,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")




# # ####### Group 5 
# # Funding Sources Percent 
### 2015
# funding_source_percent_2015 = ["Local_Property_Tax_Percent_2015", "Other_Local_Funding_Percent_2015",'General_State_Aid_Percent_2015','Other_State_Funding_Percent_2015','Federal_Funding_Percent_2015']
# for field in funding_source_percent_2015:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",10,5,5,"do_not_straddle_mean",-1,\
# 		"sequential",sequential_color_dictionary,"percent",0,100)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(funding_source_percent_2015,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2015")
# ## 2016
# funding_source_percent_2016 = ["Local_Property_Tax_Percent_2016", "Other_Local_Funding_Percent_2016",'General_State_Aid_Percent_2016','Other_State_Funding_Percent_2016','Federal_Funding_Percent_2016']
# for field in funding_source_percent_2016:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",10,5,5,"do_not_straddle_mean",-1,\
# 		"sequential",sequential_color_dictionary,"percent",0,100)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(funding_source_percent_2016,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2016")




# ###### Group 6
# # Spending Percentages (each sums to 100%)
### 2015
# spending_percentages_2015 = ["Instruction_Percent_2015", "General_Admin_Percent_2015", "Support_Services_Percent_2015","Other_Expenditures_Percent_2015"]
# for field in spending_percentages_2015:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",11,5,5,"do_not_straddle_mean",0,\
# 		"diverging",diverging_color_dictionary,"percent",None,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(spending_percentages_2015,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")
# ## 2016
# spending_percentages_2016 = ["Instruction_Percent_2016", "General_Admin_Percent_2016", "Support_Services_Percent_2016","Other_Expenditures_Percent_2016"]
# for field in spending_percentages_2016:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",11,5,5,"do_not_straddle_mean",0,\
# 		"diverging",diverging_color_dictionary,"percent",None,None)
# # add_multiple_fields_to_legend_dictionary_and_write_to_file(spending_percentages_2016,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")



##### Group 7 
# # ### Detail Spending Percentages (adding each one sums to 100%)
# # 2015
# detail_spending_percentages_2015 = 	["Education_Percent_2015", "Operations_Percent_2015", "Transportation_Percent_2015", "Debt_Service_Percent_2015", "Tort_Fund_Percent_2015", \
# 	"Munic_Retirement_And_Soc_Sec_Percent_2015", "Fire_Prevention_And_Safety_Percent_2015", "Capital_Projects_2015"]
# for field in detail_spending_percentages_2015:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",11,5,5,"do_not_straddle_mean",0,\
# 		"diverging",diverging_color_dictionary,"percent",None,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(detail_spending_percentages_2015,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")
# # 2016
# detail_spending_percentages_2016 = 	["Education_Percent_2016", "Operations_Percent_2016", "Transportation_Percent_2016", "Debt_Service_Percent_2016", "Tort_Fund_Percent_2016", \
# 	"Munic_Retirement_And_Soc_Sec_Percent_2016", "Fire_Prevention_And_Safety_Percent_2016", "Capital_Projects_2016"]
# for field in detail_spending_percentages_2016:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",11,5,5,"do_not_straddle_mean",0,\
# 		"diverging",diverging_color_dictionary,"percent",None,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(detail_spending_percentages_2016,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")



####### Group 9 a
# Student Performance 
# # # 2015
# student_performance_a_2015 = ["HS_4_Year_Grad_Rate_2015","HS_5_Year_Grad_Rate_2015","Percent_Ready_For_College_2015"]
# for field in student_performance_a_2015:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",11,5,5,"do_not_straddle_mean",-1,\
# 		"diverging",diverging_color_dictionary,"percent",None,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(student_performance_a_2015,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")
# ## 2016
# student_performance_a_2016 = ["HS_4_Year_Grad_Rate_2016","HS_5_Year_Grad_Rate_2016","Percent_Ready_For_College_2016"]
# for field in student_performance_a_2016:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",11,5,5,"do_not_straddle_mean",-1,\
# 		"diverging",diverging_color_dictionary,"percent",None,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(student_performance_a_2016,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")


# ####### Group 9 b
# # Student Performance 
# ## 2015 
# student_performance_b_2015 = ["ACT_Comp_2015"]
# for field in student_performance_b_2015:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",11,5,5,"do_not_straddle_mean",-1,\
# 		"diverging",diverging_color_dictionary,"not_percent",None,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(student_performance_b_2015,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")
# ## 2016
# student_performance_b_2016 = ["ACT_Comp_2016"]
# for field in student_performance_b_2016:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",11,5,5,"do_not_straddle_mean",-1,\
# 		"diverging",diverging_color_dictionary,"not_percent",None,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(student_performance_b_2016,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")


########## Group 10 
# # 2015
# student_tests_performance_2015 = ["Percent_Student_Met_English_Benchmark_2015", "Percent_Student_Met_Math_Benchmark_2015", \
# "Percent_Student_Met_Read_Benchmark_2015", "Percent_Student_Met_Sci_Benchmark_2015","Percent_Student_Met_All_4_Benchmark_2015"]
# for field in student_tests_performance_2015:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",11,5,5,"do_not_straddle_mean",-1,\
# 		"diverging",diverging_color_dictionary,"percent",None,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(student_tests_performance_2015,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")
# # 2016
# student_tests_performance_2016 = ["Percent_Student_Met_English_Benchmark_2016", "Percent_Student_Met_Math_Benchmark_2016", \
# "Percent_Student_Met_Read_Benchmark_2016", "Percent_Student_Met_Sci_Benchmark_2016","Percent_Student_Met_All_4_Benchmark_2016"]
# for field in student_tests_performance_2016:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",11,5,5,"do_not_straddle_mean",-1,\
# 		"diverging",diverging_color_dictionary,"percent",None,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(student_tests_performance_2016,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")



################ ARCHIVING 2014 FIELD FOR NOW ##########################
############ Group 11 - 
# ## 2014 
# student_tests_performance_2014 = ["Meets_or_Exceeds_Read_and_Math_2014"]
# for field in student_tests_performance_2014:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",11,5,5,"do_not_straddle_mean",-1,\
# 		"diverging",diverging_color_dictionary,"percent",None,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(student_tests_performance_2014,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")
## 2015
#### Didn't download for 2015...if needed can corect earlier bin step 03



# ############## Group 12 a - Teacher Stats - Segment
# ## 2015
# teacher_states_group_a_2015 = ["Ave_Class_Size_2015"]
# for field in teacher_states_group_a_2015:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"segment_districts",11,5,5,"do_not_straddle_mean",-1,\
# 		"diverging",diverging_color_dictionary,"not_percent",None,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(teacher_states_group_a_2015,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")
# ## 2016
# teacher_states_group_a_2016 = ["Ave_Class_Size_2016"]
# for field in teacher_states_group_a_2016:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"segment_districts",11,5,5,"do_not_straddle_mean",-1,\
# 		"diverging",diverging_color_dictionary,"not_percent",None,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(teacher_states_group_a_2016,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")



# ############## Group 12 b 0 - Teacher States - Do Not Segment, 0 Rounding 
### 2015, 
# teacher_stats_group_b_0_2015 = ["Teacher_Rentention_Rate_2015"]
# for field in teacher_stats_group_b_0_2015:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",11,5,5,"do_not_straddle_mean",0,\
# 		"diverging",diverging_color_dictionary,"percent",None,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(teacher_stats_group_b_0_2015,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")

# ### 2016, 
# teacher_stats_group_b_0_2016 = ["Teacher_Rentention_Rate_2016"]
# for field in teacher_stats_group_b_0_2016:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",11,5,5,"do_not_straddle_mean",0,\
# 		"diverging",diverging_color_dictionary,"percent",None,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(teacher_stats_group_b_0_2016,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")


# ############## Group 12 b 1 - Teacher States - Do Not Segment, -1 Rounding 
# ## 2015
# teacher_stats_group_b_1_2015 = ["Bach_Degree_2015"]
# for field in teacher_stats_group_b_1_2015:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",11,5,5,"do_not_straddle_mean",-1,\
# 		"diverging",diverging_color_dictionary,"percent",None,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(teacher_stats_group_b_1_2015,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")
# ## 2016,
# teacher_stats_group_b_1_2016 = ["Bach_Degree_2016"]
# for field in teacher_stats_group_b_1_2016:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",11,5,5,"do_not_straddle_mean",-1,\
# 		"diverging",diverging_color_dictionary,"percent",None,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(teacher_stats_group_b_1_2016,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")



####### Group 12 c = Teacher - Do Not Segment - Decimal point precision
# ## 2015
# teacher_states_group_c_2015 = ["Percent_Class_Not_Taught_By_High_Qual_Teacher_2015"]
# for field in teacher_states_group_c_2015:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",11,5,5,"do_not_straddle_mean",0,\
# 		"diverging",diverging_color_dictionary,"percent",None,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(teacher_states_group_c_2015,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")
# ## 2016
# ### Stat Not Available for 2016




####### Group 12 d = Teacher - Do Not Segment - Sequential 
## 2015
# teacher_states_group_d_2015 = ["Ave_Admin_Salary_2015"]
# for field in teacher_states_group_d_2015:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",10,5,5,"do_not_straddle_mean",-1,\
# 		"sequential",sequential_color_dictionary,"not_percent",None,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(teacher_states_group_d_2015,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")
# ## 2016
# teacher_states_group_d_2016 = ["Ave_Admin_Salary_2016"]
# for field in teacher_states_group_d_2016:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",10,5,5,"do_not_straddle_mean",-1,\
# 		"sequential",sequential_color_dictionary,"not_percent",None,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(teacher_states_group_d_2016,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")




########## Group 13 - Other Finance Stuff
## 2015
# other_finance_2015 = ["EAV_Per_Pupil_2015"]
# for field in other_finance_2015:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",11,5,5,"do_not_straddle_mean",-2,\
# 		"diverging",diverging_color_dictionary,"not_percent",None,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(other_finance_2015,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")
# ## 2016
# other_finance_2016 = ["EAV_Per_Pupil_2016"]
# for field in other_finance_2016:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",11,5,5,"do_not_straddle_mean",-2,\
# 		"diverging",diverging_color_dictionary,"not_percent",None,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(other_finance_2016,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")



######### Group 14 -Teacher Retention
# ## 2015
# teacher_retention_2015 = ["Teacher_Rentention_Rate_2015"]
# for field in teacher_retention_2015:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",11,5,5,"do_not_straddle_mean",-1,\
# 		"diverging",diverging_color_dictionary,"not_percent",None,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(teacher_retention_2015,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")
# ## 2016
# teacher_retention_2016 = ["Teacher_Rentention_Rate_2016"]
# for field in teacher_retention_2016:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",11,5,5,"do_not_straddle_mean",-1,\
# 		"diverging",diverging_color_dictionary,"not_percent",None,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(teacher_retention_2016,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")



########### Group 15 - Student Data 
# ##2015
# last_student_demo_data_2015 = ["LEP_Percent_2015","IEP_Percent_2015","Low_Income_Percent_2015","Homeless_Percent_2015"]
# for field in last_student_demo_data_2015:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",10,5,5,"do_not_straddle_mean",0,\
# 		"sequential",sequential_color_dictionary,"percent",None,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(last_student_demo_data_2015,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")
# ##2016
# last_student_demo_data_2016 = ["LEP_Percent_2016","IEP_Percent_2016","Low_Income_Percent_2016","Homeless_Percent_2016"]
# for field in last_student_demo_data_2016:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",10,5,5,"do_not_straddle_mean",0,\
# 		"sequential",sequential_color_dictionary,"percent",None,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(last_student_demo_data_2015,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")





########### Group 16 - School Tax Rate Per 100 Dollars
# ###2015
# school_tax_rate_per_100 = ["School_Tax_Rate_Per_100_Dollars_2015"]
# for field in school_tax_rate_per_100:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",11,5,5,"do_not_straddle_mean",0,\
# 		"diverging",diverging_color_dictionary,"percent",None,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(school_tax_rate_per_100,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")
# ##2016
# school_tax_rate_per_100 = ["School_Tax_Rate_Per_100_Dollars_2016"]
# for field in school_tax_rate_per_100:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",11,5,5,"do_not_straddle_mean",0,\
# 		"diverging",diverging_color_dictionary,"percent",None,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(school_tax_rate_per_100,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")


########### Group 17 - Teacher Experience 

#######!!! ARCHIVING 2015..NO DATA REPORTED!!!!!! ####
##2015
#### For some reason  all 2015 is blank...so you can skip
# teacher_experience_2015 = ["Ave_Teacher_Exp_2015"]
# for field in teacher_experience_2015:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",11,5,5,"do_not_straddle_mean",0,\
# 		"diverging",diverging_color_dictionary,"percent",None,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(teacher_experience_2015,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")
# ##2016
# teacher_experience_2016 = ["Ave_Teacher_Exp_2016"]
# for field in teacher_experience_2016:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",11,5,5,"do_not_straddle_mean",0,\
#  		"diverging",diverging_color_dictionary,"percent",None,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(teacher_experience_2016,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")



########### Group 18 - Pupil Teacher Ratios 
# ### 2015 
# pupil_teacher_2015 = ["Pupil_Teacher_Ratio_Elem_2015","Pupil_Teacher_Ratio_HS_2015"]
# for field in pupil_teacher_2015:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",11,5,5,"do_not_straddle_mean",0,\
#  		"diverging",diverging_color_dictionary,"percent",None,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(pupil_teacher_2015,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")
# ## 2016
# pupil_teacher_2016 = ["Pupil_Teacher_Ratio_Elem_2016","Pupil_Teacher_Ratio_HS_2016"]
# for field in pupil_teacher_2016:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",11,5,5,"do_not_straddle_mean",0,\
# 		"diverging",diverging_color_dictionary,"percent",None,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(pupil_teacher_2016,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")


########### ARCHIVING THIS FOR 2014 ############
############ Group 19 - Meets or Exceeds  
### 2014
# performance_2014 = ["Meets_or_Exceeds_Read_and_Math_2014"]
# for field in performance_2014:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",11,5,5,"do_not_straddle_mean",-1,\
# 		"diverging",diverging_color_dictionary,"percent",None,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(performance_2014,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")



########### ARCHIVING THIS FOR 2014 ############
############## Group 19 - College within....
### 2014
# college_2014 = ["Percent_College_within_12_months_2014","Percent_College_within_16_months_2014"]
# for field in college_2014:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",11,5,5,"do_not_straddle_mean",-1,\
# 		"diverging",diverging_color_dictionary,"percent",None,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(college_2014,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")
################### Not Avaialble for 2015 #############
### 2015
# college_2015 = ["Percent_College_within_12_months_2015","Percent_College_within_16_months_2015"]
# for field in college_2015:
# 	elementary_boundary_dictionary[field],secondary_boundary_dictionary[field], unified_boundary_dictionary[field] = join_colors_and_stops(field, \
# 		elementary_districts_infile,secondary_districts_infile,unified_districts_infile,"do_not_segment_districts",11,5,5,"do_not_straddle_mean",-1,\
# 		"diverging",diverging_color_dictionary,"percent",None,None)
# add_multiple_fields_to_legend_dictionary_and_write_to_file(college_2015,elementary_boundary_dictionary,secondary_boundary_dictionary, unified_boundary_dictionary,elementary_legends_dictionary,secondary_legends_dictionary,unified_legends_dictionary,"2017")





####### Beg - Append the legends dictionary into the geojson files."""
### This is the final step - Only run once at the end for speed

# update_geojson_with_legends_dictionary(elementary_legends_dictionary,elementary_districts_infile,'2017','elementary')
# update_geojson_with_legends_dictionary(secondary_legends_dictionary,secondary_districts_infile,'2017','secondary')
# update_geojson_with_legends_dictionary(unified_legends_dictionary,unified_districts_infile,'2017','unified')

########## End  - Append the legends dictionary into the geojson files."""







# # ################## Beg - Manually creating the Javacript code ###################
# # Note this is mostly for testing of webpages  

# """Run Script that you use to copy / paste into JavaScript"""
# print "Elementary"
# print javascript_output(elementary_boundary_dictionary)
# print "Secondary"
# print javascript_output(secondary_boundary_dictionary)
# print "Unified"
# print javascript_output(unified_boundary_dictionary)

# ################ End - Manually creating the Javacript code ###################











############ To Do ######################

# Usage of the word "Percentile" is handled differently for Percent and Non-Percent (maybe nit a bug deal?)
# How to let Brandon know which legends are sequential and which are divergin. 
# What to do about multi-years 


