# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 16:36:35 2023

@author: oeste
"""
# import necessary modules
import pandas as pd
import string
from fuzzywuzzy import fuzz

# define data types for columns of read-in csv files
categories = {"PROJNUM":int,	
        "ProjectID":int, 
        "ParticipantSuperTypeLUID":int, 
        "ParticipantSuperType":str, 
        "ParticipantTypeLUID":int,	
        "ParticipantType":str, 
        "Participant":str, 
}

# read in the csv file with participant information to a dataframe(df)
# leave this df alone in case things go wrong later
participants = pd.read_csv("OWEB_participants.csv", dtype=categories)

# create a df that only has the list of participant names
raw_names = participants["Participant"]

# find out how many names are initially in the data
print ("All Participant Records:", len(raw_names))

# check the number of unique names we are starting with
# some of the names may look like unique values but are actually duplicates
# these pseudo-unique values are likely caused by typos or different inputers
print("Number of Unique Participant Names Initially:", raw_names.nunique())

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

# check the number of uniques after standardizing common expressions
print("Number of Unique Names Post-Expressions:", raw_names.nunique())

# create a list of all participant names, now standardized
pre_review_list = raw_names.to_list()

# the following segments of code use the imported module, fuzzywuzzy
# this module runs through a list and compares each value to every other
# by measuring the number of character changes needed to imitate each other
# the fewer changes needed, the lower the "score" for a match
# for pairings with scores above a threshold score (chosen by you),
# it then fills in a pre-made, empty list with possible duplicates
# along with the possible duplicates, it also includes potential matches
# this script creates lists for pairings with scores 80/100 as well as 90/100
# only the 80/100 matches are used for further analysis in this project

# create an empty list to hold possible duplicates and matches
duplicates_80 = {}
# create nested for loops that runs through the list of standardized names,
# uses the fuzz module to compare each name against every other name,
# and then assigns a similarity score that determines inclusion in the list
# the similarity score for this list is 80
for i, name1 in enumerate(pre_review_list):
    for j, name2 in enumerate(pre_review_list[i+1:], i+1):
        score = fuzz.token_sort_ratio(name1, name2)
        if score > 80:
            duplicates_80.setdefault(name1, set()).add(name2)
            duplicates_80.setdefault(name2, set()).add(name1)
            
# the list is then converted into a series
# the series in then written to a csv
# in the csv, the names and possible matches are now in different columns
dup_80_list = series = pd.Series(duplicates_80)
dup_80_list.to_csv("possible_dups80.csv")

# create an empty list to hold possible duplicates and matches
duplicates_90 = {}

# create nested for loops that runs through the list of standardized names,
# uses the fuzz module to compare each name against every other name,
# and then assigns a similarity score that determines inclusion in the list
# the similarity score for this list is 90
for i, name1 in enumerate(pre_review_list):
    for j, name2 in enumerate(pre_review_list[i+1:], i+1):
        score = fuzz.token_sort_ratio(name1, name2)
        if score > 90:
            duplicates_90.setdefault(name1, set()).add(name2)
            duplicates_90.setdefault(name2, set()).add(name1)
 
# the list is then converted into a series
# the series in then written to a csv
# in the csv, the names and possible matches are now in different columns
dup_90_list = series = pd.Series(duplicates_80)
dup_90_list.to_csv("possible_dups90.csv")