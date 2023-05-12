# -*- coding: utf-8 -*-
"""
Created on Wed May 10 19:09:06 2023

@author: oeste
"""
# import necessary modules
import pandas as pd
import string

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

# read in the file containing participant information
participants = pd.read_csv("OWEB_participants.csv", dtype=categories)

# create a dataframe (df) that only contains participant names
raw_names = participants["Participant"]

# remove any extra spaces from participant names; check the number of uniques
raw_names = raw_names.str.replace(r'\W',' ',regex=True)
print("Number of Unique Participants Post-Spacing:", raw_names.nunique())

# standardize the case of names by making all names lowercase; check uniques
raw_names = raw_names.apply(lambda x: ' '.join(x.lower().split()))
print("Number of Unique Participants Post-Capitals:", raw_names.nunique())

# remove all punctuation in order to further standardize names; check uniques
punct = string.punctuation
raw_names = raw_names.str.replace('[{}]'.format(punct), '')
print("Number of Unique Names Post-Punctuation:", raw_names.nunique())

# standardize common expressions in participant names
# these four lines of code standardize variations of "corporation"
raw_names = raw_names.str.replace('corps', 'co-rps')
raw_names = raw_names.str.replace('corporation', 'corp')
raw_names = raw_names.str.replace('corp', 'corporation')
raw_names = raw_names.str.replace('co-rps', 'corps')

# these two lines of code standardize variations of "cooperative"
raw_names = raw_names.str.replace('cooperative', 'coop')
raw_names = raw_names.str.replace('coop', 'cooperative')

# these two lines of code standardize variations of "department"
raw_names = raw_names.str.replace('department', 'dept')
raw_names = raw_names.str.replace('dept', 'department')

# create new df containing all of the standardized names, duplicates included
all_names = raw_names

# define data types for columns the csv file of review duplicates
# see the ReadMe file for how to design this csv file; template in repository 
review_columns = {"change_indicator":int, 
        "pre_review":str,	
        "post_review":str, 
        "possible_matches":str, 
}

# read in the csv file for reviewed duplicates to a df
post_review_list = pd.read_csv("reviewed_dups.csv", dtype=review_columns)

# in the review file, possible matches coded with a "3" need further review
# until that happens, they are dropped from the df of reviewed duplicates
post_review_list = post_review_list.drop(index=post_review_list.loc[post_review_list['change_indicator'] == 3].index)

# create dictionary that will allow for conversion of all names
# this will allow the 60,000+ list of names to be standardized
name_tracing = dict(zip(post_review_list['pre_review'], post_review_list['post_review']))

# use the dictionary to standardize the original list of participant names
standardized_names = all_names.replace(name_tracing)

# check to see how many unique names remain post-duplicate review
# in this case, nearly 200 duplicate names were found and corrected.
print("Number of Unique Names Post-Duplicate Review:", standardized_names.nunique())