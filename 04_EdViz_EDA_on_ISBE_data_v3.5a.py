#### This script is 4 of 5 

# 1) reps the US_Census Data first           
# 2) Add GSA Data
# 3) Add IL REport Card Data                       
# 4) Clean the Data and do validation on it           <- This file
# 5) Create Cholorpleth color boundaries. 



# Install Libraries:
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np	
from scipy.stats.stats import pearsonr   # For Running Correlationship


# Store Data:  ## take original DF and run as subset taking all interesting datasets and removing dropNAs
# Found help here: http://stackoverflow.com/questions/13413590/how-to-drop-rows-of-pandas-dataframe-whose-value-of-certain-column-is-nan


################################# Beg - Import information from IL REport Card #################################################

############### Store important field  = Zero indexed


col_list_2016 = [0,1,3,4,7,9,12,29,30,31,32,33,34,35,36,47,51,55,59,63,67,139,143,199,255,311,367,387,391,395,399,403,407,451,523,531, \
	539,547,551,563,567,573,580,583,586,589,592,594,595,598,601,605,610,613,616,619,622,625,628,631,634,637,640,643,645]


col_list_2015 = [0,1,3,4,7,9,12,29,30,31,32,33,34,35,36,47,51,55,59,63,67,139,143,199,255,275,279,283,287,291,295,339,411,419,427,435, \
	439,451,455,469,477,484,487,490,493,496,498,499,502,505,509,514,517,520,523,526,529,532,535,538,541,544,547,549]

col_list_2014 = [0,1,3,4,7,9,12,505,509,896,9328,9332,9336]

col_titles_2016 = {0:'LONG_RCDTS_DO_NOT_USE_2016', 
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
	598:'Total_School_Tax_Rate_Per_100_Dollars_2016',
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



col_titles_2015 = {0:'LONG_RCDTS_DO_NOT_USE_2015', 
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
	143:'HS_4_Year_Grad_Rate_2016',
	199:'HS_5_Year_Grad_Rate_2016',
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
	502:'Total_School_Tax_Rate_Per_100_Dollars_2015',
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
	

	
col_titles_2014 =  {0:'LONG_RCDTS_DO_NOT_USE_2014', 
	1:'School_Type_Code_2014',
	3:'School_Name_2014',
	4:'District_Name_2014',
	7:'District_Type_Code_2014',
	9:'District_Type_Name_2014',
	12:'Grades_In_School_2014',
	505:'IEPP_2014',
	509:'OEPP_2014',
	896: 'Meets_or_Exceeds_Read_and_Math_2014',
	9328:'Percent_College_within_16_months_2014',
	9332:'Percent_College_within_12_months_2014',
	9336:'Percent_Freshmen_On_Track_2014',
	}






################## Beg  - Load IL Report Card Data into dataframe  ################
##### File path
il_report_card_2016_path = r"..\data\ISBE\ILReportCard\2015-2016\core_data\rc16.txt"
il_report_card_2015_path = r"..\data\ISBE\ILReportCard\2014-2015\core_data\rc15.txt"
il_report_card_2014_path = r"..\data\ISBE\ILReportCard\2013-2014\rc14.txt"

##### #Read Files = 2016 - no assessment data
il_report_card_2016 = pd.read_csv(il_report_card_2016_path, 
	header = None, 
	thousands=',', 
	sep = ';', 
	low_memory = False,
	usecols = col_list_2016)


##### #Read Files = 2015 - no assessment data
il_report_card_2015 = pd.read_csv(il_report_card_2015_path, 
	header = None, 
	thousands=',', 
	sep = ';', 
	low_memory = False,
	usecols = col_list_2015)

##### #Read Files = 2014 - Contains Assessment data
il_report_card_2014 = pd.read_csv(il_report_card_2014_path, 
	header = None, 
	thousands=',', 
	sep = ';', 
	low_memory = False,
	usecols = col_list_2014)



### Experiment to try and get rid of Null Values.......Consider removing if causes breakage
# didn't appear to do anything (positive or negative)

# il_report_card_2015.fillna('', inplace=True)
# il_report_card_2014.fillna('', inplace=True)

# for index, row in il_report_card_2015.iterrows():
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
# print len(il_report_card_2015.columns)
# print il_report_card_2015.head()
# print il_report_card_2015.columns.values

# print il_report_card_2015[143]

################## End  - Load IL Report Card Data into dataframe  ################




################### Beg - Prep data (for best format) while in DF   #####################

############### Clean 2016 ###############

# Note2 - 1 is considered a strings (uses a c,..bu)  7 is a float (only 0,1,9)

###### 4 Step in this code 1) removes whitespaces, 2) replaces $ with nothing, 3) replaces Comma with nothing 4) turn into number

il_report_card_2016[563] = il_report_card_2016[563].map(str.strip).str.replace('$','').str.replace(',','').apply(pd.to_numeric)
il_report_card_2016[567] = il_report_card_2016[567].map(str.strip).str.replace('$','').str.replace(',','').apply(pd.to_numeric)
il_report_card_2016[594] = il_report_card_2016[594].map(str.strip).str.replace('$','').str.replace(',','').apply(pd.to_numeric)
il_report_card_2016[595] = il_report_card_2016[595].map(str.strip).str.replace('$','').str.replace(',','').apply(pd.to_numeric)
il_report_card_2016[601] = il_report_card_2016[601].map(str.strip).str.replace('$','').str.replace(',','').apply(pd.to_numeric)
il_report_card_2016[605] = il_report_card_2016[605].map(str.strip).str.replace('$','').str.replace(',','').apply(pd.to_numeric)
il_report_card_2016[645] = il_report_card_2016[645].map(str.strip).str.replace('$','').str.replace(',','').apply(pd.to_numeric)

##  2 Step  1) Strip whitespace 2) turn into number
# Note - Commented section threw an error (I believe because all of them were already floats)
il_report_card_2016[139] = il_report_card_2016[139].map(str.strip).apply(pd.to_numeric)
il_report_card_2016[143] = il_report_card_2016[143].map(str.strip).apply(pd.to_numeric)
il_report_card_2016[199] = il_report_card_2016[199].map(str.strip).apply(pd.to_numeric)
il_report_card_2016[255] = il_report_card_2016[255].map(str.strip).apply(pd.to_numeric) 	#new field
il_report_card_2016[311] = il_report_card_2016[311].map(str.strip).apply(pd.to_numeric)		# new field
il_report_card_2016[367] = il_report_card_2016[367].map(str.strip).apply(pd.to_numeric)
il_report_card_2016[387] = il_report_card_2016[387].map(str.strip).apply(pd.to_numeric)
il_report_card_2016[391] = il_report_card_2016[391].map(str.strip).apply(pd.to_numeric)
il_report_card_2016[395] = il_report_card_2016[395].map(str.strip).apply(pd.to_numeric)
il_report_card_2016[399] = il_report_card_2016[399].map(str.strip).apply(pd.to_numeric)
il_report_card_2016[403] = il_report_card_2016[403].map(str.strip).apply(pd.to_numeric)
il_report_card_2016[407] = il_report_card_2016[407].map(str.strip).apply(pd.to_numeric)
# il_report_card_2016[451] = il_report_card_2016[451].map(str.strip).apply(pd.to_numeric)
# il_report_card_2016[523] = il_report_card_2016[523].map(str.strip).apply(pd.to_numeric)
il_report_card_2016[547] = il_report_card_2016[547].map(str.strip).apply(pd.to_numeric)
il_report_card_2016[551] = il_report_card_2016[551].map(str.strip).apply(pd.to_numeric)
# il_report_card_2016[563] = il_report_card_2016[563].map(str.strip).apply(pd.to_numeric)
# il_report_card_2016[567] = il_report_card_2016[567].map(str.strip).apply(pd.to_numeric)
il_report_card_2016[573] = il_report_card_2016[573].map(str.strip).apply(pd.to_numeric)
il_report_card_2016[580] = il_report_card_2016[580].map(str.strip).apply(pd.to_numeric)
il_report_card_2016[583] = il_report_card_2016[583].map(str.strip).apply(pd.to_numeric)
il_report_card_2016[586] = il_report_card_2016[586].map(str.strip).apply(pd.to_numeric)
il_report_card_2016[589] = il_report_card_2016[589].map(str.strip).apply(pd.to_numeric)
il_report_card_2016[592] = il_report_card_2016[592].map(str.strip).apply(pd.to_numeric)
il_report_card_2016[598] = il_report_card_2016[598].map(str.strip).apply(pd.to_numeric)
il_report_card_2016[610] = il_report_card_2016[610].map(str.strip).apply(pd.to_numeric)
il_report_card_2016[613] = il_report_card_2016[613].map(str.strip).apply(pd.to_numeric)
il_report_card_2016[616] = il_report_card_2016[616].map(str.strip).apply(pd.to_numeric)
il_report_card_2016[619] = il_report_card_2016[619].map(str.strip).apply(pd.to_numeric)
il_report_card_2016[622] = il_report_card_2016[622].map(str.strip).apply(pd.to_numeric)
il_report_card_2016[625] = il_report_card_2016[625].map(str.strip).apply(pd.to_numeric)
il_report_card_2016[628] = il_report_card_2016[628].map(str.strip).apply(pd.to_numeric)
il_report_card_2016[631] = il_report_card_2016[631].map(str.strip).apply(pd.to_numeric)
il_report_card_2016[634] = il_report_card_2016[634].map(str.strip).apply(pd.to_numeric)
il_report_card_2016[637] = il_report_card_2016[637].map(str.strip).apply(pd.to_numeric)
il_report_card_2016[640] = il_report_card_2016[640].map(str.strip).apply(pd.to_numeric)
il_report_card_2016[643] = il_report_card_2016[643].map(str.strip).apply(pd.to_numeric)
# il_report_card_2016[645] = il_report_card_2016[645].map(str.strip).apply(pd.to_numeric)



# 1 Step - 1) strip out whitespace
il_report_card_2016[3] = il_report_card_2016[3].map(str.strip)
il_report_card_2016[4] = il_report_card_2016[4].map(str.strip)
il_report_card_2016[9] = il_report_card_2016[9].map(str.strip)
il_report_card_2016[12] = il_report_card_2016[12].map(str.strip)

############### Clean 2015  #############

# Note - Don't need to perform on 0,55, 67, 339, 419, 427 (they are both already a Long or float)
# Note2 - 1 is considered a strings (uses a c,..bu)  7 is a float (only 0,1,9)

###### 4 Step in this code 1) removes whitespaces, 2) replaces $ with nothing, 3) replaces Comma with nothing 4) turn into number

il_report_card_2015[451] = il_report_card_2015[451].map(str.strip).str.replace('$','').str.replace(',','').apply(pd.to_numeric)
il_report_card_2015[455] = il_report_card_2015[455].map(str.strip).str.replace('$','').str.replace(',','').apply(pd.to_numeric)
il_report_card_2015[499] = il_report_card_2015[499].map(str.strip).str.replace('$','').str.replace(',','').apply(pd.to_numeric)
il_report_card_2015[505] = il_report_card_2015[505].map(str.strip).str.replace('$','').str.replace(',','').apply(pd.to_numeric)
il_report_card_2015[509] = il_report_card_2015[509].map(str.strip).str.replace('$','').str.replace(',','').apply(pd.to_numeric)
il_report_card_2015[549] = il_report_card_2015[549].map(str.strip).str.replace('$','').str.replace(',','').apply(pd.to_numeric)
il_report_card_2015[498] = il_report_card_2015[498].map(str.strip).str.replace('$','').str.replace(',','').apply(pd.to_numeric)

##  2 Step  1) Strip whitespace 2) turn into number
il_report_card_2015[139] = il_report_card_2015[139].map(str.strip).apply(pd.to_numeric)
il_report_card_2015[143] = il_report_card_2015[143].map(str.strip).apply(pd.to_numeric)
il_report_card_2015[199] = il_report_card_2015[199].map(str.strip).apply(pd.to_numeric)
il_report_card_2015[255] = il_report_card_2015[255].map(str.strip).apply(pd.to_numeric)
il_report_card_2015[275] = il_report_card_2015[275].map(str.strip).apply(pd.to_numeric)
il_report_card_2015[279] = il_report_card_2015[279].map(str.strip).apply(pd.to_numeric)
il_report_card_2015[283] = il_report_card_2015[283].map(str.strip).apply(pd.to_numeric)
il_report_card_2015[287] = il_report_card_2015[287].map(str.strip).apply(pd.to_numeric)
il_report_card_2015[291] = il_report_card_2015[291].map(str.strip).apply(pd.to_numeric)
il_report_card_2015[295] = il_report_card_2015[295].map(str.strip).apply(pd.to_numeric)
il_report_card_2015[411] = il_report_card_2015[411].map(str.strip).apply(pd.to_numeric)
il_report_card_2015[435] = il_report_card_2015[435].map(str.strip).apply(pd.to_numeric)
il_report_card_2015[439] = il_report_card_2015[439].map(str.strip).apply(pd.to_numeric)
il_report_card_2015[469] = il_report_card_2015[469].map(str.strip).apply(pd.to_numeric)
il_report_card_2015[477] = il_report_card_2015[477].map(str.strip).apply(pd.to_numeric)
il_report_card_2015[484] = il_report_card_2015[484].map(str.strip).apply(pd.to_numeric)
il_report_card_2015[487] = il_report_card_2015[487].map(str.strip).apply(pd.to_numeric)
il_report_card_2015[490] = il_report_card_2015[490].map(str.strip).apply(pd.to_numeric)
il_report_card_2015[493] = il_report_card_2015[493].map(str.strip).apply(pd.to_numeric)
il_report_card_2015[496] = il_report_card_2015[496].map(str.strip).apply(pd.to_numeric)
il_report_card_2015[514] = il_report_card_2015[514].map(str.strip).apply(pd.to_numeric)
il_report_card_2015[517] = il_report_card_2015[517].map(str.strip).apply(pd.to_numeric)
il_report_card_2015[520] = il_report_card_2015[520].map(str.strip).apply(pd.to_numeric)
il_report_card_2015[523] = il_report_card_2015[523].map(str.strip).apply(pd.to_numeric)
il_report_card_2015[526] = il_report_card_2015[526].map(str.strip).apply(pd.to_numeric)
il_report_card_2015[529] = il_report_card_2015[529].map(str.strip).apply(pd.to_numeric)
il_report_card_2015[532] = il_report_card_2015[532].map(str.strip).apply(pd.to_numeric)
il_report_card_2015[535] = il_report_card_2015[535].map(str.strip).apply(pd.to_numeric)
il_report_card_2015[538] = il_report_card_2015[538].map(str.strip).apply(pd.to_numeric)
il_report_card_2015[541] = il_report_card_2015[541].map(str.strip).apply(pd.to_numeric)
il_report_card_2015[544] = il_report_card_2015[544].map(str.strip).apply(pd.to_numeric)
il_report_card_2015[547] = il_report_card_2015[547].map(str.strip).apply(pd.to_numeric)


# 1 Step - 1) strip out whitespace
il_report_card_2015[3] = il_report_card_2015[3].map(str.strip)
il_report_card_2015[4] = il_report_card_2015[4].map(str.strip)
il_report_card_2015[9] = il_report_card_2015[9].map(str.strip)
il_report_card_2015[12] = il_report_card_2015[12].map(str.strip)


 

############ Clean 2014 ##############
# Note - Don't need to perform on 0, 7 (already a Long)

# 4 Step in this code 1) removes whitespaces, 2) replaces $ with nothing, 3) replaces Comma with nothing 4) turn into number
il_report_card_2014[896] = il_report_card_2014[896].map(str.strip).str.replace(',','').apply(pd.to_numeric)
il_report_card_2014[505] = il_report_card_2014[505].map(str.strip).str.replace('$','').str.replace(',','').apply(pd.to_numeric)
il_report_card_2014[509] = il_report_card_2014[509].map(str.strip).str.replace('$','').str.replace(',','').apply(pd.to_numeric)
# 1 Step - 1) strip out whitespace
il_report_card_2014[4] = il_report_card_2014[4].map(str.strip)
il_report_card_2014[9] = il_report_card_2014[9].map(str.strip)
il_report_card_2014[12] = il_report_card_2014[12].map(str.strip)


################### End - Prep data (for best format) while in DF   #####################



###########Create Subset Dataframes for each district Types

# # Store in separate dataframes 

"""2016"""
unified_IRC_2016_df = il_report_card_2016[il_report_card_2016[7] == 2] 			# Unit Districts
elementary_IRC_2016_df = il_report_card_2016[il_report_card_2016[7] == 0] 			# Elementary Districts
secondary_IRC_2016_df = il_report_card_2016[il_report_card_2016[7] == 1] 			# Secondary Districts

# Create a subset (for unified district only)...that take only HS 
unified_HS_IRC_2016_df = il_report_card_2016[(il_report_card_2016[1] == '0') & (il_report_card_2016[7] == 2) ].copy()  # column 1 is a string 


"""2015"""
unified_IRC_2015_df = il_report_card_2015[il_report_card_2015[7] == 2] 			# Unit Districts
elementary_IRC_2015_df = il_report_card_2015[il_report_card_2015[7] == 0] 			# Elementary Districts
secondary_IRC_2015_df = il_report_card_2015[il_report_card_2015[7] == 1] 			# Secondary Districts

# Create a subset (for unified district only)...that take only HS 
unified_HS_IRC_2015_df = il_report_card_2015[(il_report_card_2015[1] == '0') & (il_report_card_2015[7] == 2) ].copy()  # column 1 is a string 

"""2014"""
unified_IRC_2014_df = il_report_card_2014[il_report_card_2014[7] == 2] 			# Unit Districts
elementary_IRC_2014_df = il_report_card_2014[il_report_card_2014[7] == 0] 			# Elementary Districts
secondary_IRC_2014_df = il_report_card_2014[il_report_card_2014[7] == 1] 			# Secondary Districts

# Create a subset (for unified district only)...that take only HS 
unified_HS_IRC_2014_df = il_report_card_2014[(il_report_card_2014[1] == '0') & (il_report_card_2014[7] == 2) ].copy()  # column 1 is a string 



##### Peform some basic counting on number of school 

# c1 = il_report_card_2015[1].value_counts(sort=False)
# # print c1

# # # How many District Types?
# c7 = il_report_card_2015[7].value_counts(sort=False)
# print c7





###################### Beg -  Univariate Analysis ##############################################################


################### Create a function to describe a given field and plot a historgrams  #############################

def describe_and_histogram(df,field_number,field_name,axis_start_and_stop_array):
	v = df[field_number].dropna()
	print v.describe()
	n, bins, patches = plt.hist(v, 50, normed=0, facecolor='g', alpha=0.75)
	plt.xlabel(field_name)
	plt.ylabel('Frequency of occurrence')
	plt.title('Histogram of '+field_name)
	plt.axis(axis_start_and_stop_array)
	plt.grid(True)
	plt.show()
	return

	
# Run Summary Decription and Histogram

# IEPP  2015 / OEPP 2015
# describe_and_histogram(il_report_card_2015,505,'Instructional Spend Per Pupil IL 2015',[0, 20000, 0, 700])
# describe_and_histogram(il_report_card_2015,509,'Instructional Spend Per Pupil IL 2015',[0, 31000, 0, 700])


# # EAV
# describe_and_histogram(il_report_card_2015,499,'EAV in 2015',[0, 550000, 0, 1000])

# # Pupil to Teacher
# describe_and_histogram(il_report_card_2015,435,'Pupil: Teacher Ratio in 2015',[0, 50, 0, 650])

# # # Teacher Retention (unified, Secondary, Elem)
# describe_and_histogram(unified_IRC_2015_df,477,'Unified Teacher Retention 2015',[0, 100, 0, 650])
# describe_and_histogram(secondary_IRC_2015_df,477,'Secondary Teacher Retention 2015',[0, 100, 0, 30])
# describe_and_histogram(elementary_IRC_2015_df,477,'Elementary Teacher Retention 2015',[0, 100, 0, 300])

#Parental Invovlement
# describe_and_histogram(unified_IRC_2015_df,67,'Unified Parental Invovlement 2015',[0, 100, 0, 1000])
# describe_and_histogram(secondary_IRC_2015_df,67,'Secondary Parental Invovlement 2015',[0, 100, 0, 100])
# describe_and_histogram(elementary_IRC_2015_df,67,'Elementary Parental Invovlement 2015',[0, 100, 0, 900])

# Low Income Percentage
# describe_and_histogram(unified_IRC_2015_df,55,'Unified Low Income Percentage 2015',[0, 100, 0, 600])
# describe_and_histogram(secondary_IRC_2015_df,55,'Secondary Low Income Percentage 2015',[0, 100, 0, 20])
# describe_and_histogram(elementary_IRC_2015_df,55,'Elementary Low Income Percentage 2015',[0, 100, 0, 60])

# # Race
# describe_and_histogram(il_report_card_2015,29,'Percentage of White Student in District',[0, 100, 0, 600])
# describe_and_histogram(il_report_card_2015,30,'Percentage of Black Student in District',[0, 100, 0, 1500])
# describe_and_histogram(il_report_card_2015,31,'Percentage of Hispanic Student in District',[0, 100, 0, 700])
# describe_and_histogram(il_report_card_2015,32,'Percentage of Asian Student in District',[0, 100, 0, 1500])
# describe_and_histogram(il_report_card_2015,33,'Percentage of Native Hawaiian or Pacific Islander Student in District',[0, 10, 0, 1600])
# describe_and_histogram(il_report_card_2015,34,'Percentage of Native American Student in District',[0, 10, 0, 1000])
# describe_and_histogram(il_report_card_2015,35,'Percentage of Student with Two or More Races in District',[0, 20, 0, 800])


# # Disabilities
# describe_and_histogram(il_report_card_2015,47,'Percentage of LEP Students in District',[0, 100, 0, 1600])
# describe_and_histogram(il_report_card_2015,51,'Percentage of IEP Students in District',[0, 100, 0, 1000])


# # Graduation Rates
# describe_and_histogram(il_report_card_2015,143,'Percentage of HS Students graduating in 4 Years in District',[0, 100, 0, 150])
# describe_and_histogram(il_report_card_2015,199,'Percentage of HS Students graduating in 5 Years in District',[0, 100, 0, 150])


# #Pupil: teach Ratios
# describe_and_histogram(il_report_card_2015,435,'Pupil to Teacher Ratio: Elementary ',[0, 32, 0, 650])
# describe_and_histogram(il_report_card_2015,439,'Pupil to Teacher Ratio: High School',[0, 32, 0, 650])


#other school Finances
# describe_and_histogram(il_report_card_2015,499,'EAV Per Pupil 2015',[0, 2100000, 0, 1000])
# describe_and_histogram(il_report_card_2015,502,'Tax Rate per 100 of EAV',[0, 10, 0, 1000])


#Total Enrollment
# describe_and_histogram(il_report_card_2015,36,'Total Enrollment ',[0, 400000, 0, 3000])

# describe_and_histogram(il_report_card_2015,439,'Percentage of HS Students graduating in 5 Years in District',[0, 100, 0, 150])


################### Relationship Between variables  ##################################

####### Notes for Scatterplots
# Documentation of .scatter: http://matplotlib.org/api/pyplot_api.html
# Exmaple: http://matplotlib.org/examples/shapes_and_collections/scatter_demo.html
# # Example Code
# N = 50
# x = np.random.rand(N)
# y = np.random.rand(N)
# colors = np.random.rand(N)
# area = np.pi * (15 * np.random.rand(N))**2  # 0 to 15 point radiuses
# plt.scatter(x, y, s=area, c=colors, alpha=0.5)
# plt.show()

########## Notes for Pearson Correlation
# Documentation: http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.stats.pearsonr.html
# Example: http://stackoverflow.com/questions/19428029/how-to-get-correlation-of-two-vectors-in-python
# a = [1,4,6]
# b = [1,2,3]   
# print pearsonr(a,b)


################### Relationship 1: IEPP to Pupil:teacher Ratio    #######################################
# Conclusion- VERY clear relationship between IEPP and TEacher Ratio !!!  .41 
#####GOOD FOR BLOG POST!!!!!!!!!!!!!!!!!

# ##### Store Data 
# x = il_report_card_2015[505] # Instruction Expenditure Per Pupil
# y = il_report_card_2015[435]  # Pupil : Teacher Ratio - Elemenary

# #### Correlations
# pcorr = pearsonr(x,y)

# #### Scatter Plots
# plt.scatter(x, y, s = 20, alpha=0.5)
# plt.show()





################## Relationship 2:  OEPP to Pupil:Teacher Ratio - Elementary  ############################################
# Conclusion: still clear relationship not as wow  .33
#### Store Data 
# x = temp_df[509] # Operation Expenditure Per Pupil
# y = temp_df[435]  # Pupil : Teacher Ratio - Elementary

# #### Correlations
# print pearsonr(x,y)

# #### Scatter Plots
# plt.scatter(x, y, s = 20, alpha=0.5)
# plt.show()


################### Relationship 3: IEPP to Pupil: teacher Ratio - High    ################################
### Conclusion - Some relationship, .30 looks a bit more random, possibly heavy influenced by outliers


# ###### Store Data 
# x = il_report_card_2015[505]  # IEPP   
# y = il_report_card_2015[439]  # Pupil : Teacher Ratio - High

# ###### Correlation 
# print pearsonr(x,y)

# ###### #Scatter Plot
# plt.scatter(x, y, s = 20, alpha=0.5)
# plt.show()


# ################ Relationship 4:  IEPP to EAV Per Pupil     ##################################################
# # Conclusion - Very Strong Relationship   .56  more tax dollars = more to spend

# ####### Store Data
# x = il_report_card_2015[505]  # IEPP   
# y = il_report_card_2015[499]  # EAV Per Pupil

# ####### Correlations
# print pearsonr(x,y)

# ###### Scatter Plot
# plt.scatter(x, y, s = 20, alpha=0.5)
# plt.show()



################## Relationship 5: OEPP to EAV Per Pupil ################################################
# Conclusion:  Relatively strong relationship .27 (not nearly as strong as IEPP) what does that mean?  (more operational spend in wealth?)


# #### Store Data
# x = temp_df[509]  # OEPP   
# y = temp_df[439]  # Pupil : Teacher Ratio - High

# ###### Correlationship
# temp_df = il_report_card_2015.dropna(subset = [509,439])  # this removes NaN's
# print pearsonr(x,y)

# ###### Scatterplots 
# plt.scatter(x, y, s = 20, alpha=0.5)
# plt.show()

################ Relationship 6:  IEPP to Poverty %     ##################################################
# Conclusion: And Unclear relationship

	# ####### Store Data
	# x = il_report_card_2015[505]  # IEPP   
	# y = il_report_card_2015[55]  # LOW-INCOME DISTRICT %

	# ####### Correlations
	# print pearsonr(x,y)

	# ###### Scatter Plot
	# plt.scatter(x, y, s = 20, alpha=0.5)
	# plt.show()


# ############## Relationship 7:  IEPP to Teacher Salary     ##################################################
# Conclusion:   VERY srong  .89

# ####### Store Data
# x = il_report_card_2015[505]  # IEPP   
# y = il_report_card_2015[451]  # Teacher Salary

# ####### Correlations
# print pearsonr(x,y)

# ###### Scatter Plot
# plt.scatter(x, y, s = 20, alpha=0.5)
# plt.show()


################ Relationship 8:  IEPP to Teacher Retention     ##################################################
# Conclusion:  Need Pearson, but there's something there.


# ####### Store Data
# # !!!!!!!!!!!!!!!! Can't get this to WORK!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# x = il_report_card_2015[il_report_card_2015[505].notnull()]
# y = il_report_card_2015[il_report_card_2015[471].notnull()]


# print np.mean(x)
# print np.mean(y)


# ##### Correlations
# print pearsonr(x,y)

# ###### Scatter Plot
# plt.scatter(x, y, s = 20, alpha=0.5)
# plt.show()



############### Relationship 9:  Teacher Salary to  Teacher Retention     ##################################################
# Conclusion:  Need Pearson correl, but there's something there. 


# # ####### Store Data
# x = il_report_card_2015[451]  # Teacher Salary
# y = il_report_card_2015[477]  # Teacher Rentention


# ####### Correlations
# # print pearsonr(x,y)   ##########!!!!!!!!!!!! Need to fix 477 not sure why isn't working 

# # ###### Scatter Plot
# plt.scatter(x, y, s = 20, alpha=0.5)
# plt.show()




################ Relationship 10: Version 1:  IEPP to % READY FOR COLLEGE COURSE WORK - DISTRICT     ##################################################
# Conclusion:   Not sure I trust PCorrl here -.28...need's investigation,  Second version verifies,  Conclusion is IEPP is negatively correlated with College Readyiness



# # ####### Store Data
# x = il_report_card_2015[505]  # IEPP 
# y = il_report_card_2015[275]  # % HS Ready for College

# ####### Correlations
# print pearsonr(x,y)   

# # ###### Scatter Plot
# plt.scatter(x, y, s = 20, alpha=0.5)
# plt.show()

# ################ Relationship 10: Version 2:  IEPP to % READY FOR COLLEGE COURSE WORK - DISTRICT ##############################

# # Source : http://stackoverflow.com/questions/19068862/how-to-overplot-a-line-on-a-scatter-plot-in-python

# def scatter_plot_with_correlation_line(x, y, graph_filepath):
#     '''
#     http://stackoverflow.com/a/34571821/395857
#     x does not have to be ordered.
#     '''
#     # Scatter plot
#     plt.scatter(x, y)

#     # Add correlation line
#     axes = plt.gca()
#     m, b = np.polyfit(x, y, 1)
#     X_plot = np.linspace(axes.get_xlim()[0],axes.get_xlim()[1],100)
#     plt.plot(X_plot, m*X_plot + b, '-')

#     # Save figure
#     plt.savefig(graph_filepath, dpi=300, format='png', bbox_inches='tight')

# def main():
#     # Data
#     # Original 
#     # x = np.random.rand(100)
#     # y = x + np.random.rand(100)*0.1
#     # Updated
#     x = temp_df[505]  # IEPP
#     y = temp_df[139]  # % HS Ready for College

#     # Plot
#     scatter_plot_with_correlation_line(x, y, 'scatter_plot.png')

# if __name__ == "__main__":
#     main()
#     # cProfile.run('main()') # if you want to do some profiling





################ Relationship 11::  IEPP to HS Dropout Rate ##################################################
# Conclusion:   
# WWRONG variable to look at...need to examine 4 year HS completeion (dropout here means...student who moved)

# # ####### Store Data
# x = il_report_card_2015[505]  # IEPP 
# y = il_report_card_2015[139]  #  HS Dropbout Rate District


# ####### Correlations
# print pearsonr(x,y)   

# # ###### Scatter Plot
# plt.scatter(x, y, s = 20, alpha=0.5)
# plt.show()


################ Relationship 12::  2014 IEPP to  2014 DISTRICT COMPOSITE PERCENT FOR MEETS & EXCEEDS(read and math)     ##################################################

# Conclusion:   


# # ####### Store Data

# cleaned_df = il_report_card_2014.dropna
# x = cleaned_df[505]  # IEPP 
# y = cleaned_df[896]  #  HS Dropbout Rate District


# # ####### Correlations
# print pearsonr(x,y)   
# !!!!!!!!!!!!!!!!!! Not working,...get Nan !!!!!!!!!!!!!!!!!!

# # ###### Scatter Plot
# plt.scatter(x, y, s = 20, alpha=0.5)
# plt.show()




#####################  Try to get a Correlation Matrix 

# Example: http://stackoverflow.com/questions/14657433/correlation-matrix-in-python

# print temp_df.dtypes
# print np.corrcoef(temp_df)





######################## End -  Performa EDA on ISBE dataset #####################################

