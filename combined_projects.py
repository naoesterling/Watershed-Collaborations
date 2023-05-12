# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 13:19:13 2023

@author: oeste
"""
# import necessary modules
import pandas as pd

# define data types for columns of the csv file to be read in
categories = {"PROJNUM":int,	
        "ProjectID":int,
        "count_combined": int,
        "combined": int,
        "instream":str, 
        "riparian":str, 
        "passage":str,	
        "road":str, 
        "upland":str, 
        "wetland":str, 
        "estuarine":str, 
        "urban":str, 
        "screening":str, 
        "flow":str,
        "InKind":str,
}

# read in data for combined projects and create a dataframe (df) of the data
projects = pd.read_csv("comb_projects.csv", dtype=categories)

# format df by cutting unnecessary columns and setting an index
projects = projects.drop(["ProjectID", "count_combined", "combined"], axis=1)
projects = projects.set_index("PROJNUM")

# create list of all the possible types of projects that could be combined
terrain_list = ['instream','riparian','passage','road','upland','wetland','estuarine','urban','screening','flow']

# create a df that organizes the individual project type columns into one
# the df will now have a column with an aggregate type list for each project
comb_proj_list = projects[terrain_list]
comb_proj_list = comb_proj_list.fillna('')
comb_proj_list['Terrain_Type_List'] = comb_proj_list.apply(lambda x: ', '.join([str(i) for i in x.values if i != '']), axis=1)

# create a df that only contains the project IDs and their terrain type lists
proj_type_list = comb_proj_list[['Terrain_Type_List']].reset_index()

# set the project IDs as the index of this new df
proj_type_list = proj_type_list.set_index("PROJNUM")

# create df to count the number of terraint types in a combined project
# reformat the type of data in the df
# the df will now contain binary data on the presence or absence of types
# terrain types in each project with a designation of "combined"
comb_proj_count = projects[terrain_list]
replace_dict = {'instream':1,'riparian':1,'passage':1,'road':1,'upland':1,'wetland':1,'estuarine':1,'urban':1,'screening':1,'flow':1}
comb_proj_count.replace(replace_dict, inplace=True)
comb_proj_count = comb_proj_count.fillna('0')

# in order to sum the number of terrain types, convert all values to integers
comb_proj_count['instream'] = comb_proj_count['instream'].astype(int)
comb_proj_count['riparian'] = comb_proj_count['riparian'].astype(int)
comb_proj_count['passage'] = comb_proj_count['passage'].astype(int)
comb_proj_count['road'] = comb_proj_count['road'].astype(int)
comb_proj_count['upland'] = comb_proj_count['upland'].astype(int)
comb_proj_count['wetland'] = comb_proj_count['wetland'].astype(int)
comb_proj_count['estuarine'] = comb_proj_count['estuarine'].astype(int)
comb_proj_count['urban'] = comb_proj_count['urban'].astype(int)
comb_proj_count['screening'] = comb_proj_count['screening'].astype(int)
comb_proj_count['flow'] = comb_proj_count['flow'].astype(int)

# sum across the columns of different types in the df
# create a total column for the number of different terrain types
comb_proj_count["Total_Terrain_Types"] = comb_proj_count.sum(axis=1)

# merge the count df and the df with the terrain type list
merge_comb_proj = comb_proj_count.merge(proj_type_list, left_index=True, right_index=True)

# drop the individual type columns (now unnecessary given the list)
# the df is now ready to be merged into the compiled database
merge_comb_proj = merge_comb_proj.drop(['instream','riparian','passage','road','upland','wetland','estuarine','urban','screening','flow'], axis=1)