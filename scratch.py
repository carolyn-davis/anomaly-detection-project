#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 15:14:36 2021

@author: carolyndavis
"""


import warnings
warnings.filterwarnings("ignore")



import pandas as pd

import acquire as a 
import numpy as np
import datetime as t

import matplotlib.pyplot as plt 

import seaborn as sns

# =============================================================================
# Questions I am trying to answer:
# =============================================================================
# =============================================================================
# 1. What topics are grads continuing to reference after graduation and into 
# their jobs (for each program)?
#---------------------------------------------------------------------------
# 2. Which lesson appears to attract the most traffic consistently across cohorts (per program)?
#---------------------------------------------------------------------------
# 3. Is there a cohort that referred to a lesson significantly more than other
#  cohorts seemed to gloss over?
#------------------------------------------------------------------------
# 4. Are there students who, when active, hardly access the curriculum? If so, 
# what information do you have about these students?
# =============================================================================

df = a.get_curriculum_logs_data()
df.shape


df.info()

# =============================================================================
# observations
# =============================================================================
#change cols: date, time, startdt, enddt to pd.datetime
#merge date and time cols and set as index
#path defines lesson, table of contents and .json data usage, drop anthing not lesson
#domain analysis indicates cohort id and id are keys and mean the same thing according to SQL
#convert all nums to int or floats for uniformity
#program id supports domain knowledge of program type 1:PHP, 2:Java, 3:Data Science, 4:Front/End
#keep name for label analysis in congruence with numeric data
#slack seems pointless..likely drop, along with creation and deleted_at cols
#start and end date will likely tell the best story for anomalies implies activity outside normal tf



# =============================================================================
# DATA PREP: Date and Time Cols
# =============================================================================

#setting the dfindex to the date and time cols concatted together
# df = df.set_index(pd.to_datetime(df.date + ' ' + df.time))
# df.head()


#looks good, now drop the those cols 
# df = df.drop(columns=['date', 'time'], axis= 1)
# df.head()

# cohort_df = pd.read_csv('cohorts.csv')

# =============================================================================
# DATA PREP: Path Cols 
# =============================================================================

initial_drop = ['id', 'created_at', 'deleted_at', 'slack']

df = df.drop(columns=(initial_drop))

df.info()

df['program_id'] = df['program_id'].astype(str)
# =============================================================================
# Making Cols for 4 Program IDS 
# =============================================================================
df['program_id'] = df['program_id'].str.replace('1', 'php').str.replace('2', 'java').str.replace('3', 'ds').str.replace('4', 'fe')


# =============================================================================
# Removing paths that do not include lessons '/' alone indicating no lesson path
# =============================================================================

q1_df = df.copy()


#eliminates instances of user activity where curriculum is not accessed
q1_df = q1_df[q1_df['path'].str.len() > 2]

counts = q1_df['path'].value_counts()
counts.head(10).plot.bar()
# =============================================================================
# Takeaways:
    #the path java-script-i is the most frequently visitied lesson across all cohorts with a count of 18203
# =============================================================================




# #turn to df 
# q1_grouping = pd.DataFrame(q1_grouping)



# #reset the index for grouping 
# q1_grouping = q1_grouping.reset_index()

# #grouping by just these cols 
# q1_grouping.columns = ['cohort_id', 'path', 'count']


# q1_grouping.plot()


# =============================================================================
# Is there a cohort that refers to a lesson significantly more than other cohorts?
# =============================================================================

#looking at the value counts by cohort and path activity across cohorts
q2_grouping = q1_df.groupby('path')['cohort_id'].value_counts()
q2_grouping = q2_grouping.rename('counts')

q2_grouping = q2_grouping.reset_index()
q2_grouping = q2_grouping.set_index('cohort_id')
q2_grouping = q2_grouping.sort_values(by='counts', ascending=False)


#toc is top accessed lesson across cohorts


q2_grouping = q2_grouping[q2_grouping['path'] == 'toc']

q2_grouping.head(10).plot.bar()

# =============================================================================
# Takeaways:
    #Javascript i is the most significantly visited lesson referred to across all cohorts
# =============================================================================



# =============================================================================
# Q3: Are there students, when active, hardly access the curriculum?
# =============================================================================
#utilize q1_df for grouping by ip address and users with the path '/' indicating no actual lessons
#were utilized but user was active on DS.codeup db
q3_slashes = df[df['path'].str.len() < 2]

q3_slashes['path'].value_counts()
# /    45854
# f        1
# j        1
# '        1
# Name: path, dtype: int64


#drops miscellaneous characters and their respective rows that could not defined at time of calc


#assigns variable to rows containing slash in the column 'path'
q3_slashes = q3_slashes[q3_slashes['path'] == '/']

#any rows with a len less than too are hypothesised to be slashes
q3_unslashes = df[df['path'].str.len() > 2]


#visualize the groupings to ensure just / value for the col 
q3_grouping = q3_slashes.groupby('path')['ip'].value_counts()

#renaming the new column states as ip to counts for further analysis
q3_grouping = q3_grouping.rename('counts')

#reset the index 
q3_grouping = q3_grouping.reset_index()

#set index to unique identifier for each student 'ip'
q3_grouping = q3_grouping.set_index('ip')

#drop col path it is no longer relevant
q3_grouping = q3_grouping.drop(columns=['path'], axis=1)

#assigning all activity that is not a slash to its own col for overall activity comparison
q3_div = q3_unslashes['ip'].value_counts()
#renaming value_counts to div for divide marker
q3_div = q3_div.rename('div')

#concat the two new value count variables into one df, maintianing index integrity
q3_all = pd.concat([q3_grouping, q3_div], axis=1)


#make new col for activity ration based off homepage activity(no lessons) in comparison to all curriculum access based off student ip
q3_all['activity'] = q3_all['counts'] / q3_all['div']
#found some nuils, lets drop those
q3_all = q3_all.dropna()

#hypothesising any account or count activity t
q3_all = q3_all[q3_all['counts'] > 20]
q3_all['activity'].head(10)
q3_all = q3_all.sort_values(by='activity', ascending=False)


q3_all['activity'].head(10).plot.bar()
# =============================================================================
# #higher the counts(homepagevisits the higher the ratio actiivity indicating student isn't
# #accessing curriculum but is active according to curriculum log
# 
# =============================================================================





# q3_grouping = q3_grouping.rename('counts')
# q3_grouping = q3_grouping.reset_index()

# #plot and viz top 10 students 
# q3_grouping.head(10).plot.bar()



# =============================================================================
# Q4: What topics are grads continuously accessing after graduation from the curriculum?
# =============================================================================
# =============================================================================
# #Plan:
# =============================================================================
# =============================================================================
# #set dates to only after end date
# #look at lessons without '/' homepage indication 
# #group by program and lesson 
# 
# =============================================================================
#make a copy of the df that filters out lesson logs with just '/'
after_grad_df = q1_df.copy() 


after_grad_df = after_grad_df[after_grad_df['date'] > after_grad_df['end_date']]

q4_grouping = after_grad_df.groupby('program_id')['path'].value_counts()

q4_grouping = q4_grouping.rename('counts')

#reset the index 
q4_grouping = q4_grouping.reset_index()

# #set index to unique identifier for each student 'ip'
# q4_grouping = q4_grouping.set_index('')

keys = list(q4_grouping['program_id'].unique())
df_split = {key: q4_grouping[q4_grouping['program_id'] == key].sort_values(by= 'counts', ascending=False).head(3).set_index('path') for key in keys}


for program, df in df_split.items():
    df.plot.bar(title=program)
    plt.legend()
    plt.show()
    plt.close()
    
    



# =============================================================================
# Q5 Which lessons are least accessedpost grad(my interoretation of the question)?
# =============================================================================
# =============================================================================
# #plan:
    #group by lessons .tail for post grads or all students for least accessed lessons
    #accessed in curriculum logs 
    #look 
# =============================================================================
# =============================================================================
# #Plan:
    #essentially doing the exact process as seen above but with .tail()
# =============================================================================

q5_grouping = after_grad_df.groupby('program_id')['path'].value_counts()

q5_grouping = q5_grouping.rename('counts')

#reset the index 
q5_grouping = q5_grouping.reset_index()


keys = list(q5_grouping['program_id'].unique())
df_split = {key: q5_grouping[q5_grouping['program_id'] == key].sort_values(by= 'counts', ascending=False).tail(3).set_index('path') for key in keys}

print(df_split)




for program, df in df_split.items():
    df.plot.bar(title=program)
    plt.legend()
    plt.show()
    plt.close()
    






# =============================================================================
# thoughts....
# =============================================================================
# .json indicates not lesson
#forward slash with nothing following indicates not a lesson
#Anomolous detection thoughts 
#collect all rows with html or json, visualize
#possible indicative of web-scraping/malicious activity 
# include those and answer pertinent lesson questions/still traffic








df.path.value_counts().head(50)
#Takeaways ^^







# pages = df['path'].resample('d').count()
# pages.head()

# pages.plot()
# df.tail()






