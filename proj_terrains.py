# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 05:29:26 2023

@author: oeste
"""
# import necessary modules
import pandas as pd
from combined_projects import merge_comb_proj

# define data types for the columns of the csv files used
categories = {"PROJNUM":int,	
        "ActivityType":str,
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

# read in a csv with all projects and one with only combined-terrain projects
# the combined project file is constructed in combined_projects.py
proj_terrain_data = pd.read_csv("project_terrain_types.csv", dtype=categories)
proj_combined_data = pd.read_csv("comb_projects.csv")

# create a new dataframe (df) for single-terrain projects
single_terrain_projs = proj_terrain_data

# trim down the df to only contain single-terrain projects
# some projects have a "combined" listing; drop these
single_terrain_projs = single_terrain_projs.drop(single_terrain_projs.loc[single_terrain_projs['ActivityType'] == 'Combined'].index)

# other projects have different terrains in multiple rows
# these projects have no "combined" distinction
# drop duplicate PROJNUM to drop these combined-terrain projects
single_terrain_projs = single_terrain_projs.drop_duplicates("PROJNUM")

# format the single-terrain df with the standardized index
single_terrain_projs = single_terrain_projs.set_index("PROJNUM")

# format the single-terrain df columns like the combined-terrain df 
single_terrain_projs = single_terrain_projs.rename(columns = {'ActivityType':'Terrain_Type_List'})
single_terrain_projs['Terrain_Type_List'] = single_terrain_projs['Terrain_Type_List'].str.lower()

# input the value of "1" terrain type for single-terrain projects
single_terrain_projs['Total_Terrain_Types'] = 1

# combine the single-terrain and combined-terrain dfs
merged_terrains = pd.concat([single_terrain_projs, merge_comb_proj])