# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 05:02:34 2023

@author: oeste
"""
# import necessary module
import pandas as pd

# define data types for columns of the csv files to be read in
categories = {"PROJNUM":int,	
        "Goal":str, 
        "OtherGoal":str, 
        "cfsSpecified":str, 
}

# read files for participant data and project goal data into dataframes (dfs)
proj_information = pd.read_csv("project_info.csv", dtype=categories)
goal_data = pd.read_csv("project_goals.csv", dtype=categories)

# create a df that serves as base on which to merge goal data
# until the merge, this df will only have an index of project IDs
all_projects = proj_information.loc[:, ['PROJNUM']]
all_projects = all_projects.drop_duplicates()
all_projects = all_projects.set_index("PROJNUM")

# create a series with sums of the number of goals
proj_df = goal_data.loc[:, ['PROJNUM', 'Goal']]
proj_id_list = goal_data['PROJNUM'].tolist()
goal_count = pd.DataFrame({'PROJNUM': proj_id_list})
goal_sum = goal_count['PROJNUM'].value_counts()
goal_sum = goal_sum.rename('GoalCount')

# create a df only containing projects with goals
goal_df = goal_data.loc[:, ['PROJNUM', 'Goal']]
goal_df = goal_df.groupby('PROJNUM').agg(list)

# merge goal-specific data
goals_merge = pd.merge(goal_sum, goal_df, left_index=True, right_index=True)

# merge goal-specific data into a df of all project IDs
merged_proj_goals = pd.merge(all_projects, goals_merge, how='left', left_index=True, right_index=True)

#fill in any blank values for the permit count with a zero
merged_proj_goals["GoalCount"].fillna(0, inplace=True)