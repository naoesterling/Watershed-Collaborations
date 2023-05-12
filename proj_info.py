# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 14:26:21 2023

@author: oeste
"""
# import necessary module
import pandas as pd
import numpy as np

# define data types for columns of the csv file to be read in
categories = {"PROJNUM":int,	
        "ProjName":str, 
        "BasinActual":str, 
        "SubbasinActual":str, 
        "StartYear":int,	
        "CompleteYear":int,
}

# read in project the csv containing project information
# NOTE: 
# file made by deleting unwanted columns from the original, downloaded file
proj_information = pd.read_csv("project_info.csv", dtype=categories)

# set the index of the project information file to be the project IDs
proj_info = proj_information.set_index("PROJNUM")

# some project start and completion years were input incorrectly
# thus, any years listed outside of the dataset range are replaced with nulls
# any year values outside of ther range 1995 - 2021 are replaced.
proj_info.loc[(proj_info['StartYear'] < 1995) | (proj_info['StartYear'] > 2021), 'StartYear'] = np.nan
proj_info.loc[(proj_info['CompleteYear'] < 1995) | (proj_info['StartYear'] > 2021), 'CompleteYear'] = np.nan

# create a df with the changes to project years in order to merge into database
proj_characteristics = proj_info