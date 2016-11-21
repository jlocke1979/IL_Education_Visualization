#### This script is 2 of 5 

# 1) reps the US_Census Data first          
# 2) Add GSA data                               <- This file is Step 2
# 3) Add IL REport Card Data 
# 4) Clean the Data and do validation on it
# 5) Create Cholorpleth color boundaries. 



# install Libararies

import pandas as pd
import simplejson as json
import geojson



####### Get General State Aid (GSA) Funding (I believe) per pupil from  ISBE data  ###############
# Source: http://www.isbe.state.il.us/funding/html/gsa.htm
# look for file lableed Public Act 99-0524 FY17 GSA and Related Forecast

#### WARNING !!!!!!!!!!  Do not open the file below in EXCEL!!!!!!!  or will change over.
# * If you need to open CSV file do so with Apache OpenOffice

#Steps to get the file ready:
# 1. Save all the data as values (no formulas)
# 2. Delete header info
# 3. Ensure columns A and B are stored as text
# 4. Ensure any $ or % signs are removed (removing formatting)
# 5. Ensure all columns are saved as number (except Column A & B) this removes the - and coverts them to 0s


############ Warning ################# For now choosing not to add data from GSA (mostly for simplicity as it isn't pertinent to high level view and likely will be dropped from final viz )
# (GSA is only a small portion of Schools funding)


# # File path
# GSA_2016_2017_path = r"..\data\ISBE\per_pupil_expenditure\OPEN_ME_IN_APACHE_fy17-gsa-appropriation_justin_csv_v5.0.csv"

# #Read File
# GSA_2016_2017 = pd.read_csv(GSA_2016_2017_path, header = 0, thousands=',', index_col=False,
# 	names = ["NEW_13_Digit_ID", "OLD_13_Digit_ID", "District_Name", "FY_16_ADA_Used", "FY_16_Total_Paid", \
# 			"Total_Payment_for_FY_17", "Change_Compared_to_FY_16_Payments", "Change_per_Student", "Representative", \
# 			"Senator", "County", "Org_Type", "Rep_Number", "Sen_Number", "Percentage_Change", "2016_GSA_EPP", \
# 			"2017_GSA_EPP"])

# ########### Make New Column called "New_RCDT" used to match to data later ####
# # Create Column that gives length of NEW_13_Digit_ID 
# GSA_2016_2017['String_Length'] = GSA_2016_2017['NEW_13_Digit_ID'].str.len()
# # Create Function that will be applied to each row (condition where if 12 ...add a 0 in front to get to 13)
# def RCDT_number_parse_GSA_2016_2017(row):
# 	if row['String_Length'] == 13:
# 				return "~"+row["NEW_13_Digit_ID"][:-2]		# adding a ~ and  trimming off last 2 digits to match to 
# 	if row['String_Length'] == 12:
# 		return "~0"+row["NEW_13_Digit_ID"][:-2] # Adding a ~ AND 0 (so matches other tables) and trimming off last 2 digits to match to 

# # Apply it to each Row	
# GSA_2016_2017['New_RCDT'] = GSA_2016_2017.apply (lambda row: RCDT_number_parse_GSA_2016_2017(row),axis=1)

# #Validate the data 
# # print GSA_2016_2017.head()
# # # Print a specific value 
# # print GSA_2016_2017.loc[GSA_2016_2017['New_RCDT']=="~33094238026"]
# # print GSA_2016_2017.loc[GSA_2016_2017['NEW_13_Digit_ID']==3309423802600]
 






# ############ Beg - Unified Districts ###################

# # store file locations
# unified_districts_infile = r"..\data\US_Census_data\school_district_boundaries\GeoJSONs\2016\edited\2016_unified.geojson"
# # Open Files
# with open(unified_districts_infile) as f:


# # Update GEOJSON with GSA EPP  (keep track of # matches)
# n4= 0
# for feature in unified_districts['features']:
# 	for index, row in GSA_2016_2017.iterrows():
# 		if feature['properties']['New_RCDT'] ==  row["New_RCDT"]:    # create new field in geoJSON and attach RCDT ID
# 			feature['properties']['2017_GSA_EPP'] = row["2017_GSA_EPP"]
# 			feature['properties']['2016_GSA_EPP'] = row["2016_GSA_EPP"]

# 			n4 += 1     # count how many matches
# print n4 

# # store out file locations
# unified_districts_outfile = r"..\data\US_Census_data\school_district_boundaries\GeoJSONs\2016\edited\2016_unified.geojson"

# # Write the file to disk
# with open(unified_districts_outfile, 'w') as outfile1:
#      geojson.dump(unified_districts, outfile1)

# ########### End - Unified Districts ###################






############### Beg - Elementary districts #######################


# # store file locations
# elementary_districts_infile = r"..\data\US_Census_data\school_district_boundaries\GeoJSONs\2016\edited\2016_elementary.geojson"
# # Open Files
# with open(elementary_districts_infile) as f:
# 	elementary_districts = geojson.load(f)


# # # Update GEOJSON with GSA EPP  (keep track of # matches)
# n7= 0
# for feature in elementary_districts['features']:
# 	for index, row in GSA_2016_2017.iterrows():
# 		if feature['properties']['New_RCDT'] ==  row["New_RCDT"]:    # create new field in geoJSON and attach RCDT ID
# 			feature['properties']['2017_GSA_EPP'] = row["2017_GSA_EPP"]
# 			feature['properties']['2016_GSA_EPP'] = row["2016_GSA_EPP"]
# 			n7 += 1     # count how many matches
# print n7

# # store out file locations
# elementary_districts_outfile  = r"..\data\US_Census_data\school_district_boundaries\GeoJSONs\2016\edited\2016_elementary.geojson"

# # Write the file to disk
# with open(elementary_districts_outfile, 'w') as outfile2:
#      geojson.dump(elementary_districts, outfile2)





# ############# Beg-  Secondary districts #########################


# # store  in file locations
# secondary_districts_infile = r"..\data\US_Census_data\school_district_boundaries\GeoJSONs\2016\edited\2016_secondary.geojson"
# # Open Files
# with open(secondary_districts_infile) as f:
# 	secondary_districts = geojson.load(f)


# # Update GEOJSON with GSA EPP  (keep track of # matches)
# n10= 0
# for feature in secondary_districts['features']:
# 	for index, row in GSA_2016_2017.iterrows():
# 		if feature['properties']['New_RCDT'] ==  row["New_RCDT"]:    # create new field in geoJSON and attach RCDT ID
# 			feature['properties']['2017_GSA_EPP'] = row["2017_GSA_EPP"]
# 			feature['properties']['2016_GSA_EPP'] = row["2016_GSA_EPP"]

# 			n10 += 1     # count how many matches
# print n10

# # store out file locations
# secondary_districts_outfile = r"..\data\US_Census_data\school_district_boundaries\GeoJSONs\2016\edited\2016_secondary.geojson"

# # Write the file to disk
# with open(secondary_districts_outfile, 'w') as outfile3:
#      geojson.dump(secondary_districts, outfile3)



############## End -  Secondary districts #########################


###################### This completes the building in of GSA Data ################################
