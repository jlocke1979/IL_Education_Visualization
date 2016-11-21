#### This script is first of five

# 1) reps the US_Census Data first           <- This file is Step 1
# 2) Add GSA Data
# 3) Add IL REport Card Data 
# 4) Clean the Data and do validation on it
# 5) Create Cholorpleth color boundaries. 


# install Libararies

import pandas as pd
import simplejson as json
import geojson



############ Notes for connect the RCDT file (from ISBE data sources) to the XXSDLEA ID (in School District GeoJSON)   #############
# # # Source for connecting RCDT to ISBE
# # # http://www2.census.gov/geo/docs/reference/codes/files/st17_il_schdist.txt
############ Notes for connect the RCDT file (from ISBE data sources) to the UNSDLEA ID (in School District GeoJSON)   #############

###################### Thiis section begins the adding of data from IL Report Card from ISBE ######################
# For the US Census ONLY.. the year 2016-2017 is denoted as 2017.
 # ISBE dat is opposite (for 2016-2017 is denoted 2016)



##  Get RCDT and UNSDLEA Table

RCDT_UNSDLEA_table_path = r"..\data\RCDT_UNSDLEA_table\Local_Agency_Codes_for_school_districts_based_on_2017_v7.0.csv"
RCDT_UNSDLEA_table = pd.read_csv(RCDT_UNSDLEA_table_path, header = 0, thousands=',',
	names = ['XXSDLEA','New_RCDT','Source','Comments' ],
	dtype = {'XXSDLEA':str, 'New_RCDT':str, 'Source':str,'Comments':str})



##### Get District Boundaries GEOJSON  ##############

# Source: # https://www.census.gov/geo/maps-data/data/tiger-line.html
# Click on latest year (below uses 2015)
# Click on Download 
# Click on FTP Sites
# Download three files ELSD, UNSD, and SCSD
 # Illinois's state ID is 17
 # To Convert from Shapefile to GeoJSON go to this site:  https://ogre.adc4gis.com/


######################## Prep  GeoJSON:  ##############


# Functionize it?

def prep_us_census_boundary_file(year,district_type,RCDT_UNSDLEA_table_df):
	infile_path = "..\\data\\US_Census_data\\school_district_boundaries\\GeoJSONs\\"+year+"\\originals\\"+district_type+".geojson"
	
	# Open Files
	with open(infile_path) as f:
		districts = geojson.load(f)

	XXSDLEA = "Empty"
	# Match the district type to the right ID     (this is needed because for the three district types in US Census boundaries file therer are differing IDs based on different district type)
	if district_type == "unified":
		XXSDLEA = "UNSDLEA"
	if district_type == "elementary":
		XXSDLEA = "ELSDLEA"
	if district_type == "secondary":
		XXSDLEA = "SCSDLEA"

	# Iterate through GeoJSons and update with a None in  RCDT ID add ~ to XXSDLEA (could be UNSDLEA, ELSDLEA, or SCSDLEA)
	count_number_of_features = 0
	school_not_defined_location = None
	for feature in districts['features']:
		feature['properties']['New_RCDT'] =  None  # create shell for RCDT field
		feature['properties'][XXSDLEA] =  "~"+feature['properties'][XXSDLEA]  # create shell for RCDT field
		if feature['properties']['NAME'] == "School District Not Defined":		# This looks for the school district that is not defined (it is located out in the middle of the lake)
			school_not_defined_location = count_number_of_features			
		count_number_of_features += 1	

	print "Number of GeoJSON Boundary Features"
	print count_number_of_features

	# Check to Make sure removed "School District Not Defined"  only a problem on Unified school districts
	if district_type == "unified":                   
		districts['features'].pop(school_not_defined_location)


	# then interate through  GeoJSON and populate with New_RCDT  (keep track of matches for reference)
	number_of_matches = 0
	non_matched_districts = []				# initialize a list of districts that don't get matched (starts as empty)
	for feature in districts['features']:
		non_matched_districts.append([feature['properties']['NAME'],feature['properties'][XXSDLEA]])   # Append ALL district names to the "Non_matched" list (later I remove anything that did match)
		for index, row in RCDT_UNSDLEA_table_df.iterrows():
			if feature['properties'][XXSDLEA] == row["XXSDLEA"]:   # for the if the feature we are on in GeoJSON, cycle through Table and find a match on UNSDLEA
				feature['properties']['New_RCDT'] =  row["New_RCDT"]    # attach RCDT ID from table to New_RCDT field in geojson
				non_matched_districts.pop()							# removes the latest entry (which is the one just added) if there's a successful match
				number_of_matches += 1     # count how many matches
	print "Number of Matches"
	print number_of_matches

	print "Non-Matched District from US Census File"
	print non_matched_districts

	# store out file locations
	outfile_path = "..\\data\\US_Census_data\\school_district_boundaries\\GeoJSONs\\"+year+"\\edited\\"+year+"_"+district_type+".geojson"
	



	# Write the file to disk
	with open(outfile_path, 'w') as outfile:
	     geojson.dump(districts, outfile)

	return



########## Run the functions #############
# for 2017
prep_us_census_boundary_file("2017","unified",RCDT_UNSDLEA_table)
prep_us_census_boundary_file("2017","elementary",RCDT_UNSDLEA_table)
prep_us_census_boundary_file("2017","secondary",RCDT_UNSDLEA_table)

# for 2016
# prep_us_census_boundary_file("2016","unified",RCDT_UNSDLEA_table)
# prep_us_census_boundary_file("2016","elementary",RCDT_UNSDLEA_table)
# prep_us_census_boundary_file("2016","secondary",RCDT_UNSDLEA_table)

# for 2015
# prep_us_census_boundary_file("2015","unified",RCDT_UNSDLEA_table)
# prep_us_census_boundary_file("2015","elementary",RCDT_UNSDLEA_table)
# prep_us_census_boundary_file("2015","secondary",RCDT_UNSDLEA_table)




########## results 
# 2017
# Unified  = 383 out of 384 
	# Not sure hy is 1 short...I believe because there is a School district called "District Not Defined that is over Lake Michigan"
# Elementary = 371 out of 271
# Secondary = 99 out of 102
	# Need to Address these:
	# [['Flanagan-Cornell District 74 in Cornell', '~17901'], 
	#  ['Flanagan-Cornell District 74 in Rooks Creek', '~17903'], 
	#  ['Flanagan-Cornell District 74 in Pontiac', '~17902']]
	#Can't seem to match these...data from ISBE just has 1 district 



# 2016          
# Unified =  383 out of 383 
	# perfect..
# Elementary =  371 out of 372
	# perfect
# Secondary =  99 matches out of 102
	# [['Flanagan-Cornell District 74 in Cornell', '~17901'], 
	# ['Flanagan-Cornell District 74 in Rooks Creek', '~17903'], 
	# ['Flanagan-Cornell District 74 in Pontiac', '~17902']]

# 2015          
# Unified =  381 matches out of 386
	# ['West Richland Community Unit School District 2', '~41730'], 
	# ['Atwood-Hammond Community Unit School District 39', '~04590']]

# Elementary =  370 out of 375
	# ['Cherry School District 92', '~09720'], 
	# ['Milford Community Consolidated School District 280', '~25950']]

# Secondary =  99 matches out of 103  
	# [['Flanagan-Cornell District 74 in Cornell', '~17901'], 
	# ['Flanagan-Cornell District 74 in Rooks Creek', '~17903'], 
	# ['Milford Township High School District 233', '~25980'], 
	# ['Flanagan-Cornell District 74 in Pontiac', '~17902']]










####### below are steps to ouput information contained in US Census GeoJSON into excel CSV #################
# The purpose: is to use these to assist with the manual creation of a table matching US Census ID (UNSDLEA, ELSDLEA, SCSDLEA) to the ISBE ids (called RCDT) 



################################## Unified ########################

# # store file locations
# unified_districts_infile = r"..\data\US_Census_data\school_district_boundaries\GeoJSONs\2017\originals\unified.geojson"

# # Open Files
# with open(unified_districts_infile) as f:
# 	unified_districts = geojson.load(f)

# unified_district_name = []
# unified_district_UNSDLEA = []
# unified_district_INTPTLAT = []
# unified_district_INTPTLON = []


#  # Iterate through GeoJSons and update with a None in  RCDT ID add ~ to UNSDLEA
# for feature in unified_districts['features']:
# 	feature['properties']['UNSDLEA'] =  "~"+feature['properties']['UNSDLEA']  # Replaced float with text and tilde in front
# 	unified_district_name.append(feature['properties']['NAME'])
# 	unified_district_UNSDLEA.append(feature['properties']['UNSDLEA'])
# 	unified_district_INTPTLAT.append(feature['properties']['INTPTLAT'])
# 	unified_district_INTPTLON.append(feature['properties']['INTPTLON'])



# unified_df = pd.DataFrame({'NAME' : unified_district_name,
#  'UNSDLEA' : unified_district_UNSDLEA, 
#  'INTPTLAT' :  unified_district_INTPTLAT,
#  'INTPTLON' :  unified_district_INTPTLON,
#  })


# # # store out file locations
# unified_districts_outfile = r"..\data\RCDT_UNSDLEA_table\from_US_Census_2017\unified_basic_info.csv"

# # Write to file
# unified_df.to_csv(unified_districts_outfile,sep=",")







################################## Elementary ########################
# store file locations
# elementary_districts_infile = r"..\data\US_Census_data\school_district_boundaries\GeoJSONs\2017\originals\elementary.geojson"
# # Open Files
# with open(elementary_districts_infile) as f:
# 	elementary_districts = geojson.load(f)


# elementary_district_name = []
# elementary_district_ELSDLEA = []
# elementary_district_INTPTLAT = []
# elementary_district_INTPTLON = []


#  # Iterate through GeoJSons and update with a None in  RCDT ID add ~ to UNSDLEA
# for feature in elementary_districts['features']:
# 	feature['properties']['ELSDLEA'] =  "~"+feature['properties']['ELSDLEA']  # Replaced float with text and tilde in front
# 	elementary_district_name.append(feature['properties']['NAME'])
# 	elementary_district_ELSDLEA.append(feature['properties']['ELSDLEA'])
# 	elementary_district_INTPTLAT.append(feature['properties']['INTPTLAT'])
# 	elementary_district_INTPTLON.append(feature['properties']['INTPTLON'])

# # Tunr into Dataframe
# elementary_df = pd.DataFrame({'NAME' : elementary_district_name,
#  'ELSDLEA' : elementary_district_ELSDLEA, 
#  'INTPTLAT' :  elementary_district_INTPTLAT,
#  'INTPTLON' :  elementary_district_INTPTLON,
#  })


# # store out file locations
# elementary_districts_outfile = r"..\data\RCDT_UNSDLEA_table\from_US_Census_2017\elementary_basic_info.csv"

# # Write the file to disk
# elementary_df.to_csv(elementary_districts_outfile,sep=",")





# ################################### Secondary ########################
# # store file locations
# secondary_districts_infile = r"..\data\US_Census_data\school_district_boundaries\GeoJSONs\2017\originals\secondary.geojson"
# # Open Files
# with open(secondary_districts_infile) as f:
# 	secondary_districts = geojson.load(f)


# secondary_district_name = []
# secondary_district_SCSDLEA = []
# secondary_district_INTPTLAT = []
# secondary_district_INTPTLON = []


#  # Iterate through GeoJSons and update with a None in  RCDT ID add ~ to UNSDLEA
# for feature in secondary_districts['features']:
# 	feature['properties']['SCSDLEA'] =  "~"+feature['properties']['SCSDLEA']  # Replaced float with text and tilde in front
# 	secondary_district_name.append(feature['properties']['NAME'])
# 	secondary_district_SCSDLEA.append(feature['properties']['SCSDLEA'])
# 	secondary_district_INTPTLAT.append(feature['properties']['INTPTLAT'])
# 	secondary_district_INTPTLON.append(feature['properties']['INTPTLON'])

# # Tunr into Dataframe
# secondary_df = pd.DataFrame({'NAME' : secondary_district_name,
#  'ELSDLEA' : secondary_district_SCSDLEA, 
#  'INTPTLAT' :  secondary_district_INTPTLAT,
#  'INTPTLON' :  secondary_district_INTPTLON,
#  })


# # store out file locations
# secondary_districts_outfile = r"..\data\RCDT_UNSDLEA_table\from_US_Census_2017\secondary_basic_info.csv"

# # Write the file to disk
# secondary_df.to_csv(secondary_districts_outfile,sep=",")



