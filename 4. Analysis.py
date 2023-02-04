#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 22:23:52 2022

Code created by: Olivia Gunther, Sarah Lueling, Sarah Scott
"""

import pandas as pd
import os
import statsmodels.formula.api as smf

'''
4. Analysis

In this final section, we create a clean dataset with all of our values, and
then run an OLS regression to predict voter turnout numbers, controlling for 
GDP, unemployment rates, and whether or not there is a Democratic president in
office. We also run an OLS regression to predict student enrollment, again
controlling for GDP, unemployment rates, and whether or not there is a
Democratic president in office.

'''

# scrape information on US presidents from Wikipedia

#BASE_PATH = r'/Users/scotty/Documents/Github/final-project-college-enrollment-political-parties'
BASE_PATH = r'/Users/oliviagunther/Documents/GitHub/final-project-college-enrollment-political-parties'


def create_ols_dataset(econ_data, pres_data, voting_data, enrollment_data):

    econ_data['key'] = 1
    pres_data['key'] = 1
    econ_pres_merged_df = pd.merge(econ_data, pres_data, on='key').drop("key", 1)
    econ_pres_merged_df = econ_pres_merged_df[
        (econ_pres_merged_df['DATE'] >= econ_pres_merged_df['Start_Year']) &
        (econ_pres_merged_df['DATE'] <= econ_pres_merged_df['End_Year'])]

    econ_pres_voting_merged_df = pd.merge(
        econ_pres_merged_df,
        voting_data,
        how="inner",
        on=None,
        left_on='DATE',
        right_on='Year',
    )

    full_df = pd.merge(
        econ_pres_voting_merged_df,
        enrollment_data,
        how="inner",
        on=None,
        left_on='DATE',
        right_on='years',
    )

    full_df = full_df[['DATE', 'GDP', 'UNRATE', 'is_demo', 'Total_voting_pop_18_24_yo', 'enrollment']]

    return full_df

# import csvs
econ_measures = pd.read_csv(os.path.join(BASE_PATH, 'Clean_Data/econ_measures.csv'))
student_enrollment_df_clean = pd.read_csv(os.path.join(BASE_PATH, 'Clean_Data/student_enrollment_df_clean.csv'))
full_voting_data_clean = pd.read_csv(os.path.join(BASE_PATH, 'Clean_Data/full_voting_data_clean.csv'))
president_df_clean = pd.read_csv(os.path.join(BASE_PATH, 'Clean_Data/president_df_clean.csv'))

# convert all date columns to datetime
econ_measures['DATE'] = pd.to_datetime(econ_measures.DATE)
student_enrollment_df_clean['years'] = pd.to_datetime(student_enrollment_df_clean.years)
full_voting_data_clean['Year'] = pd.to_datetime(full_voting_data_clean.Year)

president_df_clean["Start_Year"] = pd.to_datetime(president_df_clean.Start_Year)
president_df_clean["End_Year"] = pd.to_datetime(president_df_clean.End_Year)

# filter econ_measures for only January data
econ_measures['month'] = econ_measures['DATE'].dt.month
econ_measures = econ_measures[econ_measures['month'] == 1]

all_metrics = create_ols_dataset(econ_measures,
                                 president_df_clean,
                                 full_voting_data_clean,
                                 student_enrollment_df_clean)

# all_metrics tweets to csv
folderpath = os.path.join(BASE_PATH, 'Clean_Data')
all_metrics.to_csv(os.path.join(folderpath, 'all_metrics.csv'))

# OLS regression to predict voter turnout rates
voter_turnout_results = smf.ols('Total_voting_pop_18_24_yo ~ GDP + UNRATE + is_demo',
                                data=all_metrics).fit()

# Inspect the results
print(voter_turnout_results.summary())

# OLS regression to predict college student enrollment data
enrollment_results = smf.ols('enrollment ~ GDP + UNRATE + is_demo',
                             data=all_metrics).fit()

# Inspect the results
print(enrollment_results.summary())
