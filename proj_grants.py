# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 08:38:20 2023

@author: oeste
"""
# import necessary module
import pandas as pd

# define data types for columns of read-in csv files
categories = {"PROJNUM":int,	
        "GrantNum":str
}

# read files for participant data and project goal data into dataframes (dfs)
proj_information = pd.read_csv("project_info.csv", dtype=categories)
grant_data = pd.read_csv("project_grants.csv", dtype=categories)

# create a df that serves as base on which to merge grant data
# until the merge, this df will only have an index of project IDs
all_projects = proj_information.loc[:, ['PROJNUM']]
all_projects = all_projects.drop_duplicates()
all_projects = all_projects.set_index("PROJNUM")

# create a series with sums of the number of grants
proj_df = grant_data.loc[:, ['PROJNUM', 'GrantNum']]
proj_df = proj_df.dropna(subset=['GrantNum'])
proj_id_list = proj_df['PROJNUM'].tolist()
grant_count = pd.DataFrame({'PROJNUM': proj_id_list})
grant_sum = grant_count['PROJNUM'].value_counts()
grant_sum = grant_sum.rename('GrantCount')

# create a df only containing projects with grants
grant_df = grant_data.loc[:, ['PROJNUM', 'GrantNum']]
grant_df = grant_df.dropna(subset=['GrantNum'])
grant_df = grant_df.groupby('PROJNUM').agg(list)

# merge grant-specific data
grants_merge = pd.merge(grant_sum, grant_df, left_index=True, right_index=True)

# merge grant-specific data into a df of all project IDs
merged_proj_grants = pd.merge(all_projects, grants_merge, how='left', left_index=True, right_index=True)

#fill in any blank values for the permit count with a zero
merged_proj_grants["GrantCount"].fillna(0, inplace=True)