#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 22:23:52 2022

Code created by: Olivia Gunther, Sarah Lueling, Sarah Scott
"""

# citations
# https://www.geeksforgeeks.org/create-a-pandas-dataframe-from-lists/
# https://en.wikipedia.org/wiki/List_of_presidents_of_the_United_States
# https://www.geeksforgeeks.org/create-a-pandas-dataframe-from-lists/
# https://www.geeksforgeeks.org/iterate-over-a-list-in-python/
# https://bobbyhadz.com/blog/python-remove-everything-after-character
# https://stackoverflow.com/questions/19469697/return-multiple-lists-in-python-function
# https://www.geeksforgeeks.org/creating-a-pandas-dataframe-using-list-of-tuples/
# https://stackoverflow.com/questions/19961490/construct-pandas-dataframe-from-list-of-tuples-of-row-col-values
# https://stackoverflow.com/questions/52643775/how-to-replace-specific-character-in-pandas-column-with-null
# https://www.geeksforgeeks.org/split-a-text-column-into-two-columns-in-pandas-dataframe/
# https://datatofish.com/read_excel/
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html
# https://stackoverflow.com/questions/41815079/pandas-merge-join-two-data-frames-on-multiple-columns
# https://stackoverflow.com/questions/18250298/how-to-check-if-a-value-is-in-the-list-in-selection-from-pandas-data-frame
# https://stackoverflow.com/questions/18265935/how-do-i-create-a-list-with-numbers-between-two-values
# https://stackoverflow.com/questions/16729574/how-can-i-get-a-value-from-a-cell-of-a-dataframe
# https://www.census.gov/data/tables/time-series/demo/voting-and-registration/p20-585.html
# https://matplotlib.org/stable/tutorials/intermediate/legend_guide.html
# https://matplotlib.org/stable/gallery/text_labels_and_annotations/custom_legends.html
# https://stackoverflow.com/questions/22642511/change-y-range-to-start-from-0-with-matplotlib
# https://www.folkstalk.com/2022/10/python-legend-being-cut-off-with-code-examples.html
# https://stackoverflow.com/questions/25146121/extracting-just-month-and-year-separately-from-pandas-datetime-column
# https://www.geeksforgeeks.org/python-program-to-perform-cross-join-in-pandas/
# https://shiny.rstudio.com/py/docs/ui-page-layouts.html
# https://medium.com/swlh/quick-text-pre-processing-c444f0ed9dcc
# https://shiny.rstudio.com/py/api/
# https://stackoverflow.com/questions/12201928/open-gives-filenotfounderror-ioerror-errno-2-no-such-file-or-directory
# https://medium.com/dataseries/how-to-scrape-millions-of-tweets-using-snscrape-195ee3594721

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
