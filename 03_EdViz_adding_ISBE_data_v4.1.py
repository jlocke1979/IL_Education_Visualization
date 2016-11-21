#### This script is 3 of 5 

# 1) reps the US_Census Data first           
# 2) Add GSA Data
# 3) Add IL REport Card Data                       <- This file
# 4) Clean the Data and do validation on it
# 5) Create Cholorpleth color boundaries. 




# Install libraries 
import pandas as pd
import simplejson as json
import geojson
import csv


###################### Thiis section begins the adding of data from IL Report Card from ISBE ######################
 # For  ISBE dat is opposite (for 2016-2017 is denoted 2016)
# For the US Census ONLY.. the year 2016-2017 is denoted as 2017.

############################### Begining  Store  the locatin of desired fields (IL RPT Card) Note = Zero inclusive in count####################

col_list_core_2016 = [0,1,3,4,7,9,12,29,30,31,32,33,34,35,36,47,51,55,59,63,67,139,143,199,255,311,367,387,391,395,399,403,407,451,523,531, \
	539,547,551,563,567,573,580,583,586,589,592,594,595,598,601,605,610,613,616,619,622,625,628,631,634,637,640,643,645]

col_list_core_2015 = [0,1,3,4,7,9,12,29,30,31,32,33,34,35,36,47,51,55,59,63,67,139,143,199,255,275,279,283,287,291,295,339,411,419,427,435, \
	439,451,455,469,477,484,487,490,493,496,498,499,502,505,509,514,517,520,523,526,529,532,535,538,541,544,547,549]


# Archiving 2014 for now
# col_list_assessment_2014 = [0,1,3,4,7,9,12,505,509,896,9328,9332,9336]


col_titles_core_2016 = {0:'LONG_RCDTS_DO_NOT_USE_2016', 
	1:'School_Type_Code_2016',
	3:'School_Name_2016',
	4:'District_Name_2016',
	7:'District_Type_Code_2016',
	9:'District_Type_Name_2016',
	12:'Grades_In_School_2016',
	# Student Data: Race
	29:'District_White_Percent_2016',
	30:'District_Black_Percent_2016',
	31:'District_Hispanic_Percent_2016',
	32:'District_Asian_Percent_2016',
	33:'District_Native_Hawaiian_or_Pac_Islander_Percent_2016',
	34:'District_Native_American_Percent_2016',
	35:'District_Two_or_More_Races_Percent_2016',
	36:'District_Total_Enrollment_2016', 
	# Student Data: Disabilities	
	47:'LEP_Percent_2016',
	51:'IEP_Percent_2016',
	# Student Data: other
	55:'Low_Income_Percent_2016',
	59:'Homeless_Percent_2016',
	63:'Total_School_Days_2016',
	67:'Parental_Invovlment_Percent_2016',
	139:'Dropout_Rate_Percent_2016',  # Dropout rate is not what it sounds like ...refers to students moving out of a district
	# Student Data: Performance
	143:'HS_4_Year_Grad_Rate_2016',
	199:'HS_5_Year_Grad_Rate_2016',
	255:'HS_6_Year_Grad_Rate_2016',		# NEw Field 
	311:'HS_7_Year_Grad_Rate_2016',		# NEw Field 

	367:'ACT_Comp_2016',								# New # Here forward 
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
	}



col_titles_core_2015 = {0:'LONG_RCDTS_DO_NOT_USE_2015', 
	1:'School_Type_Code_2015',
	3:'School_Name_2015',
	4:'District_Name_2015',
	7:'District_Type_Code_2015',
	9:'District_Type_Name_2015',
	12:'Grades_In_School_2015',
	# Student Data: Race
	29:'District_White_Percent_2015',
	30:'District_Black_Percent_2015',
	31:'District_Hispanic_Percent_2015',
	32:'District_Asian_Percent_2015',
	33:'District_Native_Hawaiian_or_Pac_Islander_Percent_2015',
	34:'District_Native_American_Percent_2015',
	35:'District_Two_or_More_Races_Percent_2015',
	36:'District_Total_Enrollment_2015', 
	# Student Data: Disabilities	
	47:'LEP_Percent_2015',
	51:'IEP_Percent_2015',
	# Student Data: other
	55:'Low_Income_Percent_2015',
	59:'Homeless_Percent_2015',
	63:'Total_School_Days_2015',
	67:'Parental_Invovlment_Percent_2015',
	139:'Dropout_Rate_Percent_2015',  # Dropout rate is not what it sounds like ...refers to students moving out of a district
	# Student Data: Performance
	143:'HS_4_Year_Grad_Rate_2015',
	199:'HS_5_Year_Grad_Rate_2015',
	255:'ACT_Comp_2015',
	275:'Percent_Ready_For_College_2015',
	279:'Percent_Student_Met_English_Benchmark_2015',
	283:'Percent_Student_Met_Math_Benchmark_2015',
	287:'Percent_Student_Met_Read_Benchmark_2015',
	291:'Percent_Student_Met_Sci_Benchmark_2015',
	295:'Percent_Student_Met_All_4_Benchmark_2015',

	# Teacher States 
	339:'Ave_Class_Size_2015',
	411:'Ave_Teacher_Exp_2015',
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
	498:'Total_Revenue_Source_2015',

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
	549:'Total_Expenditures_2015',

	}
	

	
# col_titles_assessment_2014 =  {0:'LONG_RCDTS_DO_NOT_USE_2014', 
# 	1:'School_Type_Code_2014',
# 	3:'School_Name_2014',
# 	4:'District_Name_2014',
# 	7:'District_Type_Code_2014',
# 	9:'District_Type_Name_2014',
# 	12:'Grades_In_School_2014',
# 	505:'IEPP_2014',
# 	509:'OEPP_2014',
# 	896: 'Meets_or_Exceeds_Read_and_Math_2014',
# 	9328:'Percent_College_within_16_months_2014',
# 	9332:'Percent_College_within_12_months_2014',
# 	9336:'Percent_Freshmen_On_Track_2014',
# 	}






##### Store the names of all Column Titles used 2015 and 2016 and 2017
col_titles_all = []


for key, value in col_titles_core_2016.items():    	# Cycle throught 2016 column titles
	col_titles_all.append(value)					# Append to array

for key, value in col_titles_core_2015.items():    	# Cycle throught 2016 column titles
	col_titles_all.append(value)					# Append to array

# for key, value in col_titles_assessment_2014.items():		# Cycle through 2014 column title
# 	col_titles_all.append(value)					# Append it to array
	


############################ End-  Store  the locatin of desired fields Note = Zero inclusive in count####################




################## Beg  - Load IL Report Card Data into dataframe  ################
##### File path
il_report_card_core_2016_path = r"..\data\ISBE\ILReportCard\2015-2016\core_data\rc16.txt"
il_report_card_core_2015_path = r"..\data\ISBE\ILReportCard\2014-2015\core_data\rc15.txt"
# il_report_card_assessment_2014_path = r"..\data\ISBE\ILReportCard\2013-2014\rc14.txt"

##### #Read Files = 2016 - no assessment data
il_report_card_core_2016 = pd.read_csv(il_report_card_core_2016_path, 
	header = None, 
	thousands=',', 
	sep = ';', 
	low_memory = False,
	usecols = col_list_core_2016)


##### #Read Files = 2015 - no assessment data
il_report_card_core_2015 = pd.read_csv(il_report_card_core_2015_path, 
	header = None, 
	thousands=',', 
	sep = ';', 
	low_memory = False,
	usecols = col_list_core_2015)

##### #Read Files = 2014 - Contains Assessment data
# il_report_card_assessment_2014 = pd.read_csv(il_report_card_assessment_2014_path, 
# 	header = None, 
# 	thousands=',', 
# 	sep = ';', 
# 	low_memory = False,
# 	usecols = col_list_assessment_2014)



### Experiment to try and get rid of Null Values.......Consider removing if causes breakage
# didn't appear to do anything (positive or negative)

# il_report_card_core_2015.fillna('', inplace=True)
# il_report_card_assessment_2014.fillna('', inplace=True)

# for index, row in il_report_card_core_2015.iterrows():
# 	if row[0] == '440630190242001':
# 		print "This is a test"
# 		print row[143]
# 		print "This is a test"
		
 #Didn't work but trying to find the null values in ISBE,...answer for this example it doesn't exist because no ISBE data

#Need to find example that has ISBE but row is blank



# Note - Consider DROP DUPLICATES 
# Reason for duplicates is data file stores at school level, but we are only interested in district data)
# Therefore going through schools and updating...probably not hurting anything, but could be improved for speed



####### Validate the files 
# print len(il_report_card_core_2015.columns)
# print il_report_card_core_2015.head()
# print il_report_card_core_2015.columns.values

# print il_report_card_core_2015[143]

################## End  - Load IL Report Card Data into dataframe  ################




################### Beg - Prep data (for best format) while in DF   #####################

############### Clean 2016 ###############

# Note2 - 1 is considered a strings (uses a c,..bu)  7 is a float (only 0,1,9)

###### 4 Step in this code 1) removes whitespaces, 2) replaces $ with nothing, 3) replaces Comma with nothing 4) turn into number

il_report_card_core_2016[563] = il_report_card_core_2016[563].map(str.strip).str.replace('$','').str.replace(',','').apply(pd.to_numeric)
il_report_card_core_2016[567] = il_report_card_core_2016[567].map(str.strip).str.replace('$','').str.replace(',','').apply(pd.to_numeric)
il_report_card_core_2016[594] = il_report_card_core_2016[594].map(str.strip).str.replace('$','').str.replace(',','').apply(pd.to_numeric)
il_report_card_core_2016[595] = il_report_card_core_2016[595].map(str.strip).str.replace('$','').str.replace(',','').apply(pd.to_numeric)
il_report_card_core_2016[601] = il_report_card_core_2016[601].map(str.strip).str.replace('$','').str.replace(',','').apply(pd.to_numeric)
il_report_card_core_2016[605] = il_report_card_core_2016[605].map(str.strip).str.replace('$','').str.replace(',','').apply(pd.to_numeric)
il_report_card_core_2016[645] = il_report_card_core_2016[645].map(str.strip).str.replace('$','').str.replace(',','').apply(pd.to_numeric)

##  2 Step  1) Strip whitespace 2) turn into number
# Note - Commented section threw an error (I believe because all of them were already floats)
il_report_card_core_2016[139] = il_report_card_core_2016[139].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2016[143] = il_report_card_core_2016[143].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2016[199] = il_report_card_core_2016[199].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2016[255] = il_report_card_core_2016[255].map(str.strip).apply(pd.to_numeric) 	#new field
il_report_card_core_2016[311] = il_report_card_core_2016[311].map(str.strip).apply(pd.to_numeric)		# new field
il_report_card_core_2016[367] = il_report_card_core_2016[367].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2016[387] = il_report_card_core_2016[387].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2016[391] = il_report_card_core_2016[391].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2016[395] = il_report_card_core_2016[395].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2016[399] = il_report_card_core_2016[399].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2016[403] = il_report_card_core_2016[403].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2016[407] = il_report_card_core_2016[407].map(str.strip).apply(pd.to_numeric)
# il_report_card_core_2016[451] = il_report_card_core_2016[451].map(str.strip).apply(pd.to_numeric)
# il_report_card_core_2016[523] = il_report_card_core_2016[523].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2016[547] = il_report_card_core_2016[547].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2016[551] = il_report_card_core_2016[551].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2016[573] = il_report_card_core_2016[573].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2016[580] = il_report_card_core_2016[580].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2016[583] = il_report_card_core_2016[583].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2016[586] = il_report_card_core_2016[586].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2016[589] = il_report_card_core_2016[589].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2016[592] = il_report_card_core_2016[592].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2016[598] = il_report_card_core_2016[598].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2016[610] = il_report_card_core_2016[610].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2016[613] = il_report_card_core_2016[613].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2016[616] = il_report_card_core_2016[616].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2016[619] = il_report_card_core_2016[619].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2016[622] = il_report_card_core_2016[622].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2016[625] = il_report_card_core_2016[625].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2016[628] = il_report_card_core_2016[628].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2016[631] = il_report_card_core_2016[631].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2016[634] = il_report_card_core_2016[634].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2016[637] = il_report_card_core_2016[637].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2016[640] = il_report_card_core_2016[640].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2016[643] = il_report_card_core_2016[643].map(str.strip).apply(pd.to_numeric)
# il_report_card_core_2016[645] = il_report_card_core_2016[645].map(str.strip).apply(pd.to_numeric)

	


# 1 Step - 1) strip out whitespace
il_report_card_core_2016[3] = il_report_card_core_2016[3].map(str.strip)
il_report_card_core_2016[4] = il_report_card_core_2016[4].map(str.strip)
il_report_card_core_2016[9] = il_report_card_core_2016[9].map(str.strip)
il_report_card_core_2016[12] = il_report_card_core_2016[12].map(str.strip)

############### Clean 2015  #############

# Note - Don't need to perform on 0,55, 67, 339, 419, 427 (they are both already a Long or float)
# Note2 - 1 is considered a strings (uses a c,..bu)  7 is a float (only 0,1,9)

###### 4 Step in this code 1) removes whitespaces, 2) replaces $ with nothing, 3) replaces Comma with nothing 4) turn into number

il_report_card_core_2015[451] = il_report_card_core_2015[451].map(str.strip).str.replace('$','').str.replace(',','').apply(pd.to_numeric)
il_report_card_core_2015[455] = il_report_card_core_2015[455].map(str.strip).str.replace('$','').str.replace(',','').apply(pd.to_numeric)
il_report_card_core_2015[499] = il_report_card_core_2015[499].map(str.strip).str.replace('$','').str.replace(',','').apply(pd.to_numeric)
il_report_card_core_2015[505] = il_report_card_core_2015[505].map(str.strip).str.replace('$','').str.replace(',','').apply(pd.to_numeric)
il_report_card_core_2015[509] = il_report_card_core_2015[509].map(str.strip).str.replace('$','').str.replace(',','').apply(pd.to_numeric)
il_report_card_core_2015[549] = il_report_card_core_2015[549].map(str.strip).str.replace('$','').str.replace(',','').apply(pd.to_numeric)
il_report_card_core_2015[498] = il_report_card_core_2015[498].map(str.strip).str.replace('$','').str.replace(',','').apply(pd.to_numeric)

##  2 Step  1) Strip whitespace 2) turn into number
il_report_card_core_2015[139] = il_report_card_core_2015[139].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2015[143] = il_report_card_core_2015[143].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2015[199] = il_report_card_core_2015[199].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2015[255] = il_report_card_core_2015[255].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2015[275] = il_report_card_core_2015[275].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2015[279] = il_report_card_core_2015[279].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2015[283] = il_report_card_core_2015[283].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2015[287] = il_report_card_core_2015[287].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2015[291] = il_report_card_core_2015[291].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2015[295] = il_report_card_core_2015[295].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2015[411] = il_report_card_core_2015[411].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2015[435] = il_report_card_core_2015[435].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2015[439] = il_report_card_core_2015[439].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2015[469] = il_report_card_core_2015[469].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2015[477] = il_report_card_core_2015[477].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2015[484] = il_report_card_core_2015[484].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2015[487] = il_report_card_core_2015[487].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2015[490] = il_report_card_core_2015[490].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2015[493] = il_report_card_core_2015[493].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2015[496] = il_report_card_core_2015[496].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2015[502] = il_report_card_core_2015[502].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2015[514] = il_report_card_core_2015[514].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2015[517] = il_report_card_core_2015[517].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2015[520] = il_report_card_core_2015[520].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2015[523] = il_report_card_core_2015[523].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2015[526] = il_report_card_core_2015[526].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2015[529] = il_report_card_core_2015[529].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2015[532] = il_report_card_core_2015[532].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2015[535] = il_report_card_core_2015[535].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2015[538] = il_report_card_core_2015[538].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2015[541] = il_report_card_core_2015[541].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2015[544] = il_report_card_core_2015[544].map(str.strip).apply(pd.to_numeric)
il_report_card_core_2015[547] = il_report_card_core_2015[547].map(str.strip).apply(pd.to_numeric)


# 1 Step - 1) strip out whitespace
il_report_card_core_2015[3] = il_report_card_core_2015[3].map(str.strip)
il_report_card_core_2015[4] = il_report_card_core_2015[4].map(str.strip)
il_report_card_core_2015[9] = il_report_card_core_2015[9].map(str.strip)
il_report_card_core_2015[12] = il_report_card_core_2015[12].map(str.strip)


 

############ Clean 2014 ##############
# Note - Don't need to perform on 0, 7 (already a Long)

# # 4 Step in this code 1) removes whitespaces, 2) replaces $ with nothing, 3) replaces Comma with nothing 4) turn into number
# il_report_card_assessment_2014[896] = il_report_card_assessment_2014[896].map(str.strip).str.replace(',','').apply(pd.to_numeric)
# il_report_card_assessment_2014[505] = il_report_card_assessment_2014[505].map(str.strip).str.replace('$','').str.replace(',','').apply(pd.to_numeric)
# il_report_card_assessment_2014[509] = il_report_card_assessment_2014[509].map(str.strip).str.replace('$','').str.replace(',','').apply(pd.to_numeric)


# ##  2 Step  1) Strip whitespace 2) turn into number
# il_report_card_assessment_2014[9328] = il_report_card_assessment_2014[9328].map(str.strip).apply(pd.to_numeric)
# il_report_card_assessment_2014[9332] = il_report_card_assessment_2014[9332].map(str.strip).apply(pd.to_numeric)
# il_report_card_assessment_2014[9336] = il_report_card_assessment_2014[9336].map(str.strip).apply(pd.to_numeric)

# # 1 Step - 1) strip out whitespace
# il_report_card_assessment_2014[4] = il_report_card_assessment_2014[4].map(str.strip)
# il_report_card_assessment_2014[9] = il_report_card_assessment_2014[9].map(str.strip)
# il_report_card_assessment_2014[12] = il_report_card_assessment_2014[12].map(str.strip)



################### End - Prep data (for best format) while in DF   #####################



###########Create Subset Dataframes for each district Types

# # Store in separate dataframes 

"""2016"""
unified_IRC_2016_df = il_report_card_core_2016[il_report_card_core_2016[7] == 2] 			# Unit Districts
elementary_IRC_2016_df = il_report_card_core_2016[il_report_card_core_2016[7] == 0] 			# Elementary Districts
secondary_IRC_2016_df = il_report_card_core_2016[il_report_card_core_2016[7] == 1] 			# Secondary Districts

# Create a subset (for unified district only)...that take only HS 
unified_HS_IRC_2016_df = il_report_card_core_2016[(il_report_card_core_2016[1] == '0') & (il_report_card_core_2016[7] == 2) ].copy()  # column 1 is a string 


"""2015"""
unified_IRC_2015_df = il_report_card_core_2015[il_report_card_core_2015[7] == 2] 			# Unit Districts
elementary_IRC_2015_df = il_report_card_core_2015[il_report_card_core_2015[7] == 0] 			# Elementary Districts
secondary_IRC_2015_df = il_report_card_core_2015[il_report_card_core_2015[7] == 1] 			# Secondary Districts

# Create a subset (for unified district only)...that take only HS 
unified_HS_IRC_2015_df = il_report_card_core_2015[(il_report_card_core_2015[1] == '0') & (il_report_card_core_2015[7] == 2) ].copy()  # column 1 is a string 

# """2014"""
# unified_IRC_2014_df = il_report_card_assessment_2014[il_report_card_assessment_2014[7] == 2] 			# Unit Districts
# elementary_IRC_2014_df = il_report_card_assessment_2014[il_report_card_assessment_2014[7] == 0] 			# Elementary Districts
# secondary_IRC_2014_df = il_report_card_assessment_2014[il_report_card_assessment_2014[7] == 1] 			# Secondary Districts

# # Create a subset (for unified district only)...that take only HS 
# unified_HS_IRC_2014_df = il_report_card_assessment_2014[(il_report_card_assessment_2014[1] == '0') & (il_report_card_assessment_2014[7] == 2) ].copy()  # column 1 is a string 


###################### Beg -  Create column called "District_number" for matching .....(trimms last 4 digits of ID and adds a '~' in front for matching other format) ###############################################

###### For REference#########
# District number can be obtained from School ID number Follow in the code for School ID (for comments starting number = 1)
# 1-2 = Region - Example: Dupage (19)
# 3-5 = County - Example: Dupage (022)
# 6-9 = District Number - Example: Lake Park District 108 (1080) 
# 10-11 = Type - Example: High School (Community) (16)
# 12-15 = School - Example Lake Park High School (0001)
# For details see file "R-C-D-T-S _codes.pdf" ...stored here: C:\Users\Justin\Development\EducationViz\data\ISBE


# make sure SCHOOL ID is alway 15 characters
# VERIFIED #
# for index, row in il_report_card_core_2015.iterrows():
# 	if len(row[0]) != 15:
# 		print "warning something isnt 15 characters"


# Create a function that takes School id (column 0) and trims of the last 4 digits
def RCDT_number_parse(row):
	RCDT_number = '~'+row[0][0:11]   # Note add the '~' because I did this in matching table RCDT to Census ID (e.g. UNSDLEA)..helped to have excel not convert to float and then round using scientific notation 
	return RCDT_number

# Apply the function using Lambda
il_report_card_core_2016['New_RCDT'] = il_report_card_core_2016.apply (lambda row: RCDT_number_parse (row),axis=1)
il_report_card_core_2015['New_RCDT'] = il_report_card_core_2015.apply (lambda row: RCDT_number_parse (row),axis=1)
# il_report_card_assessment_2014['New_RCDT'] = il_report_card_assessment_2014.apply (lambda row: RCDT_number_parse (row),axis=1)

unified_HS_IRC_2016_df['New_RCDT'] = unified_HS_IRC_2016_df.apply (lambda row: RCDT_number_parse (row),axis=1)
unified_HS_IRC_2015_df['New_RCDT'] = unified_HS_IRC_2015_df.apply (lambda row: RCDT_number_parse (row),axis=1)
# unified_HS_IRC_2014_df['New_RCDT'] = unified_HS_IRC_2014_df.apply (lambda row: RCDT_number_parse (row),axis=1)

# # Inspect to ensure worked
# for index, row in il_report_card_core_2015.iterrows():
# 	if len(row['RCDT']) != 12:
# 		print ' someting went wrong '
# # Verified Worked
# print il_report_card_assessment_2014.head()


###################### End -  Create column called "District_number" ###############################################





###################### Beg = Create dictionary that stores New_RCDT as Key and ISBE data as Values....#############################
#Notes - this is a temp dictionary that eventually goes into GeoJSON  ##


def update_district_dictionary(dataframe_of_interest,column_list,column_titles,district_dictionary_to_update):
	for index, row in dataframe_of_interest.iterrows():
		temp_container = {}
		for column in column_list:  					# Cycle through each value in col_list
			title = column_titles[column]				# take value in Col_list and lookup the title of that column
			if row[column] != row[column]: 				# Test to check for 'Nan' and that it isn't just blanks 
				temp_container[title] = None			# If it is then set the temp container value to None (Make sure not to use "NaN")...JSON specs don't like NaN
			else:
				temp_container[title] = row[column]		# Otherwise update the temp container with the data from IL_repot_card


		if row['New_RCDT'] in district_dict:			# Check to see if an entry already exist if so up that
			district_dict[row['New_RCDT']].update(temp_container)   
		else:
			district_dict[row['New_RCDT']] = temp_container   # Otherwise create a new entry for that ID in district_dict 
	return 


# initialize Distriction_dictionary
district_dict = {}

### Run function to update district dictionary
# 2016 - Core
update_district_dictionary(il_report_card_core_2016,col_list_core_2016,col_titles_core_2016,district_dict)
update_district_dictionary(unified_HS_IRC_2016_df,col_list_core_2016,col_titles_core_2016,district_dict)  # this updates with HS Unified  due to fact that some field are only available on some line (i.e. HS stats are on HS schools not elementary)

# 2015 - Core
update_district_dictionary(il_report_card_core_2015,col_list_core_2015,col_titles_core_2015,district_dict)
update_district_dictionary(unified_HS_IRC_2015_df,col_list_core_2015,col_titles_core_2015,district_dict)  # this updates with HS Unified  due to fact that some field are only available on some line (i.e. HS stats are on HS schools not elementary)
# # 2014 - Assessment
# update_district_dictionary(il_report_card_assessment_2014,col_list_assessment_2014,col_titles_assessment_2014,district_dict)
# update_district_dictionary(unified_HS_IRC_2014_df,col_list_assessment_2014,col_titles_assessment_2014,district_dict)  # this updates with HS Unified  due to fact that some field are only available on some line (i.e. HS stats are on HS schools not elementary)


# # Test the functions
# print district_dict['~11021301026']




# Create Calculated Field




################### Beg - Update US Census district Files with ISBE data then Export  ####################
# Created a function that does this


def update_us_census_with_ISBE_data(district_type,year,column_titles_array, district_dict_reference):

	# Crate infile path
	infile_path = "..\\data\\US_Census_data\\school_district_boundaries\\GeoJSONs\\"+year+"\\edited\\"+year+"_"+district_type+".geojson"

	# Open Files
	with open(infile_path) as f:
		districts = geojson.load(f)

	# Start by cycling through and updating each entry in GeoJSON with "None" 
	# This makes sure each entry has an key, even if the value is none
	for key_name in column_titles_array:
		for feature in districts['features']:
			feature["properties"][key_name] = None

	# Update the School District (GEOJSON) File with IL Rept Card Data
	for feature in districts['features']:					# Cycle through each school district in US Census GeoJSON
		district_of_interest = feature['properties']['New_RCDT']	# Store the New_RCDT for each school district
		for key, value in district_dict_reference.items():					# Cycle through district dictionary that contains IL Rpt Crd data
			if key == district_of_interest:							# if the key matches the district we are interested in...
				feature['properties'].update(value)					# update the entry in GeoJSON with information stored in District Dict
	

	# store out file locations
	outfile_path = "..\\output\\"+year+"_"+district_type+".geojson"
	

	# Write the file to disk
	with open(outfile_path, 'w') as outfile:
	     geojson.dump(districts, outfile)

	return



# Run the functions
### Note Year here refers to year for US Census data which for 2016-2017 is represented as 2017
# 2017
update_us_census_with_ISBE_data("unified","2017",col_titles_all,district_dict)
update_us_census_with_ISBE_data("elementary","2017",col_titles_all,district_dict)
update_us_census_with_ISBE_data("secondary","2017",col_titles_all,district_dict)


# # 2016
# update_us_census_with_ISBE_data("unified","2016",col_titles_all,district_dict)
# update_us_census_with_ISBE_data("elementary","2016",col_titles_all,district_dict)
# update_us_census_with_ISBE_data("secondary","2016",col_titles_all,district_dict)
# # ### 2015
# update_us_census_with_ISBE_data("unified","2015",col_titles_all,district_dict)
# update_us_census_with_ISBE_data("elementary","2015",col_titles_all,district_dict)
# update_us_census_with_ISBE_data("secondary","2015",col_titles_all,district_dict)




# print district_dict['~48072150025']



################### End - Update US Census district Files with ISBE data then Export ####################







# For testing on matches ...mostly data validation ...can archive otherwise

# ####### Beg -  Convert the district dictionary  to a Excel do for examination  ####

# keys = district_dict['~30077101026'].keys() 	# Store the head Using one entry as an example
# keys.insert(0,"RCDT")							# put the RCDT at the beginning
# f = csv.writer(open("IL_reportcard_2015_trimmed.csv", "wb+"))     # open afile prepping to write to it
# f.writerow(keys)												# Write the header
# for key, value in district_dict.items():						# prepare cyling through the dictionary (key = RCDT, value = a dictionary with more key value pairs)
# 	temp_line = [] 												# initialize an array for temporary storage (eventually will write this line)
# 	temp_line.append(key)										# Make the firs entry the RDCT number
# 	for sub_key, sub_value in value.items():					# Then cycle throught each of the vlues that will eventually become columns
# 		temp_line.append(sub_value)								# Append the values on the temp_line

# 	f.writerow(temp_line)										# Write the templine to the csv.



###### End -  Convert the district dictionary  to a Excel do for examination  ####













###################### Beg - Investigation Notes from Version 1.0 #########################
# !!!! Below is the investigation performed on thematches from a DIFFERENT Source:
# !!! I need to extend this investigataion at some point to ensure all districts are matching !!!!!!!


# # of the 378 make sure there's no "None"'s
# n2 = 0
# for feature in unified_districts['features']:
# 	 if  feature['properties']['RCDT'] == None: 
# 	 	print feature['properties']['UNSDLEA']
# 	 	print feature['properties']['NAME']
# 	 	n2 += 1 
# print n2


# ####################### Beg - Check for Nan's in IL ReportCard ###########################
# for index, row in il_report_card_core_2015.iterrows():
# 	# print row[0], row[0][:11], row[4]
# 	if row[0][:11] == '01001001026':
# 		print 'found it', row[4], row[0][:11], row[505]
# 	if row[0][:11] == '15016900025':
# 		print 'found it', row[4], row[0][:11], row[505]

# Conclusion:  they are coming up as blanks non Nan's so probalem must be occurring further downstream
# 010010010260001
# Payson CUSD 1                    
# 010010010262002
# Payson CUSD 1             

# OEPP
# ~15016900025 Horizon Science Acad-McKinley Pk
# ~34049900025 Prairie Crossing Charter School
# ~32038124026 Milford Area PSD 124
# ~50082115002 Whiteside SD 115
# ~15016901025 Horizon Science Acad-Belmont
####################### End - CCheck for Nan's in IL ReportCard ###########################



################### Search for NaN's   in District_Dict #####################

# import numpy as np
# print "OEPP"
# for key, value in district_dict.items():
# 	if np.isnan(value['OEPP_2015']):
# 		print key, value['District_Name']
# print "IEPP"
# for key, value in district_dict.items():
# 	if np.isnan(value['IEPP_2015']):
# 		print key, value['District_Name']
# print "Ave_Teacher_Salary"
# for key, value in district_dict.items():
# 	if np.isnan(value['Ave_Teacher_Salary']):
# 		print key, value['District_Name']

# # Results are:
# OEPP
# ~15016900025 Horizon Science Acad-McKinley Pk
# ~34049900025 Prairie Crossing Charter School
# ~32038124026 Milford Area PSD 124
# ~50082115002 Whiteside SD 115
# ~15016901025 Horizon Science Acad-Belmont
# IEPP
# ~15016900025 Horizon Science Acad-McKinley Pk
# ~32038124026 Milford Area PSD 124
# ~50082115002 Whiteside SD 115
# ~15016901025 Horizon Science Acad-Belmont
# Ave_Teacher_Salary
# ~13095029003 Hoyleton Cons SD 29


# for index, row in il_report_card_core_2015.iterrows():
# 	if row['New_RCDT'] == '~15016900025' or row['New_RCDT']=='~34049900025':
# 		print row[4], row[509], row[505]


# district_dict[row['New_RCDT']] = {'OEPP_2015':row[509], 'IEPP_2015':row[505], \
# 	"District_Name":row[4], "Pupil_Teacher_Ratio_Elem": row[435], 'Pupil_Teacher_Ratio_High_School':row[439], 'Ave_Teacher_Salary': row[451]} 


#################### Count the number of entries in district dictionary ###
# print district_dict
# n = 0
# for entry in district_dict:
# 	n+=1 
# print n
# Answer as of 7-20-2015 = 859 
#!!!! INvestigate that you got all districts at some point!!!!!!!!!!!!!!

###################### End - Investigation Notes from Version 1.0 #########################

