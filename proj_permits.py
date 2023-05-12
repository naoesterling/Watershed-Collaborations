# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 12:42:56 2023

@author: oeste
"""
# import necessary module
import pandas as pd

# define data types for columns of read-in csv files
categories = {"PermitID":int, 
        "PROJNUM":int,	
        "ProjectID":int, 
        "PermitTypeLUID":int, 
        "PermitType":str, 
        "PermitNumber":str,	
        "PermitDescriptor":str, 
        "Remark":str,
}

# read files for participant data and project permit data into dataframes (dfs)
proj_information = pd.read_csv("project_info.csv", dtype=categories)
permit_data = pd.read_csv("project_permits.csv", dtype=categories)

# create a df that serves as base on which to merge permit data
# until the merge, this df will only have an index of project IDs
all_projects = proj_information.loc[:, ['PROJNUM']]
all_projects = all_projects.drop_duplicates()
all_projects = all_projects.set_index("PROJNUM")

# create a series with sums of the number of permits
proj_df = permit_data.loc[:, ['PROJNUM', 'PermitNumber']]
proj_df = permit_data.dropna(subset=['PermitNumber'])
proj_id_list = permit_data['PROJNUM'].tolist()
permit_count = pd.DataFrame({'PROJNUM': proj_id_list})
permit_sum = permit_count['PROJNUM'].value_counts()
permit_sum = permit_sum.rename('PermitCount')

# create a df only containing projects with permits
permit_df = permit_data.loc[:, ['PROJNUM', 'PermitNumber']]
permit_df = permit_df.dropna(subset=['PermitNumber'])
permit_df = permit_df.groupby('PROJNUM').agg(list)

# merge permit-specific data
permits_merge = pd.merge(permit_sum, permit_df, left_index=True, right_index=True)

# merge permit-specific data into a df of all project IDs
merged_proj_permits = pd.merge(all_projects, permits_merge, how='left', left_index=True, right_index=True)

#fill in any blank values for the permit count with a zero
merged_proj_permits["PermitCount"].fillna(0, inplace=True)