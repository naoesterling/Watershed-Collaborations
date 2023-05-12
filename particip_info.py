# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 21:03:31 2023

@author: oeste
"""
# import necessary modules
import pandas as pd
import string
punct = string.punctuation
from particip_name_trace import name_tracing

# define data types for columns of read-in csv files
categories = {"ParticipantID":str, 
        "PROJNUM":int,	
        "ProjectID":int, 
        "ParticipantSuperTypeLUID":int, 
        "ParticipantSuperType":str, 
        "ParticipantTypeLUID":int,	
        "ParticipantType":str, 
        "Participant":str, 
        "ProgramName":str, 
        "GrantNum":str, 
        "NameExtraInfo":str, 
        "Contact":str, 
        "Cash":str,
        "InKind":str,
        "Respondent	Landowner":str,
        "Funder":str,
        "Project Coordinator":str,
        "Technical Support":str,
        "OWEB Grantee":str,
        "ODFW FSPP Applicant":str
}

# read in the csv file with participant information to a dataframe(df)
# leave this df alone in case things go wrong later
particip_data = pd.read_csv("OWEB_participants.csv", dtype=categories)

# create a df to work in that only has the columns you need/find important
# this cleaning process will focus on participant names and sector types
proj_df = particip_data[["PROJNUM", "Participant", "ParticipantType"]]

# remove any extra spaces from participant names
proj_df["Participant"] = proj_df["Participant"].str.replace(r'\W',' ',regex=True)

# standardize the case of names by making all names lowercase
proj_df["Participant"] = proj_df["Participant"].apply(lambda x: ' '.join(x.lower().split()))

# remove all punctuation in order to further standardize names
proj_df["Participant"] = proj_df["Participant"].str.replace('[{}]'.format(punct), '')

# standardize common expressions in participant names
# these four lines of code standardize variations of "corporation"
proj_df["Participant"] = proj_df["Participant"].str.replace('corps', 'co-rps')
proj_df["Participant"] = proj_df["Participant"].str.replace('corporation', 'corp')
proj_df["Participant"] = proj_df["Participant"].str.replace('corp', 'corporation')
proj_df["Participant"] = proj_df["Participant"].str.replace('co-rps', 'corps')

# these two lines of code standardize variations of "cooperative"
proj_df["Participant"] = proj_df["Participant"].str.replace('cooperative', 'coop')
proj_df["Participant"] = proj_df["Participant"].str.replace('coop', 'cooperative')

# these two lines of code standardize variations of "department"
proj_df["Participant"] = proj_df["Participant"].str.replace('department', 'dept')
proj_df["Participant"] = proj_df["Participant"].str.replace('dept', 'department')

# combine participant names with their sectoral types
proj_df['NameType'] = proj_df['Participant'] + ' (' + proj_df['ParticipantType'] + ')'

# earlier, the name_tracing dictionary was imported
# using this dictionary, participant names are standardized
# this removes duplication and allows for improved user searches
proj_df["Participant"] = proj_df["Participant"].replace(name_tracing)

# for each project, create a list of name-type pairings for all participant
proj_members = proj_df.groupby('PROJNUM')['NameType'].apply(list)

# create a new df with name-type pairings to be used for database construction
proj_participants = pd.DataFrame(proj_members, columns=["NameType"])