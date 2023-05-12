# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 21:27:17 2023

@author: oeste
"""
# import necessary module
import pandas as pd

# import dataframe (df) outputs from other scripts in the repository
from proj_info import proj_characteristics
from proj_terrains import merged_terrains
from proj_goals import merged_proj_goals
from proj_permits import merged_proj_permits
from proj_grants import merged_proj_grants
from particip_info import proj_participants

# merge grant and permit dfs
merged_grants_permits = pd.merge(merged_proj_grants, merged_proj_permits, left_index=True, right_index=True)

# merge project descriptions and participant information dfs
merged_descrips_particips = pd.merge(proj_characteristics, proj_participants, left_index=True, right_index=True)

# merge project terrain type and project goal dfs
merged_terrain_goals  = pd.merge(merged_proj_goals, merged_terrains, left_index=True, right_index=True)

# merge grant-permit df and description-participant dfs
merged_proj_data_1 = pd.merge(merged_grants_permits, merged_descrips_particips, left_index=True, right_index=True)

# merge grant-permit-description-participant df with terrain-goal df
# this completes the construction of this particular version of the database
merged_proj_data_2 = pd.merge(merged_proj_data_1, merged_terrain_goals, left_index=True, right_index=True)

# write the constructed database into a csv file
merged_proj_data_2.to_csv("project_database.csv")