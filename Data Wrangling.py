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
import requests
from bs4 import BeautifulSoup
import numpy as np
import os
import re
from datetime import datetime
import pandas_datareader.data as web

'''
1. Data Wrangling

In this section, we will:
    - scrape the Wikipedia page on US presidents
    - use an API to pull GDP and unemployment data from FRED
    - import voter turnout data from Census Bureau
    - import student enrollment data

'''

BASE_PATH = r'/Users/oliviagunther/Documents/GitHub/final-project-college-enrollment-political-parties'
# BASE_PATH = r"/Users/scotty/Documents/GitHub/final-project-college-enrollment-political-parties"

# scrape information on US presidents from Wikipedia


def scrape_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    # isolate necessary table
    tables = soup.find_all("table")
    table = tables[0]
    rows = table.find_all("tr")

    return rows


def clean_president_data(president_rows, inputs):
    president_names = []
    president_parties = []
    president_election_yrs = []

    for tuple_item in inputs:

        if tuple_item[0] == "president_names":
            separator = "("
            for i in range(1, len(president_rows)):
                items = president_rows[i].find_all(tuple_item[1])
                president_names.append(items[tuple_item[2]].text.split(separator, 1)[0])

        elif tuple_item[0] == "president_parties":
            for i in range(1, len(president_rows)):
                items = president_rows[i].find_all(tuple_item[1])
                president_parties.append(items[tuple_item[2]].text)
        else:
            for i in range(1, len(president_rows)):
                items = president_rows[i].find_all(tuple_item[1])
                president_election_yrs.append(
                    items[tuple_item[2]].text.split(separator, 1)[0]
                )

    return president_names, president_parties, president_election_yrs


def presidential_data_to_clean_df(initial_tuple):
    presidents_df = pd.DataFrame(initial_tuple)
    presidents_df = presidents_df.T
    presidents_df.columns = ["President Name", "Party", "Election_Year"]

    presidents_df = presidents_df[39:]

    presidents_df[["Start_Year", "End_Year"]] = presidents_df.Election_Year.str.split(
        expand=True
    )

    presidents_df = presidents_df.drop("Election_Year", axis=1)
    presidents_df["Start_Year"] = presidents_df["Start_Year"].replace("–", np.NaN)
    presidents_df["End_Year"] = presidents_df["End_Year"].replace("None", np.NaN)
    presidents_df["Start_Year"] = presidents_df["Start_Year"].astype(float)
    presidents_df["End_Year"] = presidents_df["End_Year"].astype(float)
    presidents_df.End_Year.fillna(presidents_df.Start_Year, inplace=True)
    presidents_df.loc[presidents_df["End_Year"] > 0, "End_Year"] = (
        presidents_df["End_Year"] + 4
    )
    presidents_df["Start_Year"] = presidents_df["Start_Year"] + 1

    presidents_df["color"] = np.where(
        presidents_df["Party"] == "Republican\n", "red", "blue"
    )
    presidents_df["is_demo"] = np.where(presidents_df["Party"] == "Republican\n", 0, 1)
    presidents_df = presidents_df[(presidents_df["Start_Year"] > 2000)]
    presidents_df["Start_Year"] = pd.to_datetime(presidents_df.Start_Year,
                                                 format="%Y")
    presidents_df["End_Year"] = pd.to_datetime(presidents_df.End_Year,
                                               format="%Y")

    return presidents_df


url = r"https://en.wikipedia.org/wiki/List_of_presidents_of_the_United_States"
list_of_inputs = [
    ("president_names", "td", 1),
    ("president_parties", "td", 4),
    ("president_election_yrs", "td", 5),
]

presidential_raw_data = scrape_data(url)
presidents = clean_president_data(presidential_raw_data, list_of_inputs)
president_df_clean = presidential_data_to_clean_df(presidents)

# president_df_clean to csv
folderpath = os.path.join(BASE_PATH, "Clean_Data")
president_df_clean.to_csv(os.path.join(folderpath, "president_df_clean.csv"),
                                       index=False)


# pull GDP and unemployment rate from FRED


def API_data_pull():

    start = datetime(2000, 1, 1)
    end = datetime(2020, 12, 31)

    series = ["GDP", "UNRATE", "CPALTT01USM657N", "JHDUSRGDPBR"]

    fred_dataset = web.DataReader(series, "fred", start, end)
    fred_dataset = fred_dataset.dropna().reset_index()
    return fred_dataset


econ_measures = API_data_pull()

# econ_measures to csv
econ_measures.to_csv(os.path.join(folderpath, "econ_measures.csv"),
                     index=False)


# Voter turnout by age from 2000-2020


def import_clean_voter_data(file_path):
    # import voter data
    voting_info_df = pd.read_excel(file_path)

    # clean voter data
    voter_turnout_df = voting_info_df[73:102]
    voter_turnout_df = voter_turnout_df.iloc[:, :4]
    voter_turnout_df.columns = [
        "Year",
        "Total_voting_pop_18_24_yo",
        "perc_total_voted",
        "perc_total_citizen_voted",
    ]

    # clean registered voter data
    registered_voter_df = voting_info_df[107:136]
    registered_voter_df = registered_voter_df.iloc[:, :4]
    registered_voter_df.columns = [
        "Year",
        "Total_voting_pop_18_24_yo",
        "perc_total_reg",
        "perc_total_citizen_reg",
    ]

    # merge voter turnout and registered voter data sets
    full_voting_data = voter_turnout_df.merge(
        registered_voter_df,
        left_on=["Year", "Total_voting_pop_18_24_yo"],
        right_on=["Year", "Total_voting_pop_18_24_yo"],
    )

    # clean full voting dataset
    full_voting_data = full_voting_data.astype(np.float64)

    # distinguish presidential from midterm election cycles
    election_years = np.arange(1964, 2024, 4).tolist()
    midterm_years = np.arange(1966, 2026, 4).tolist()
    full_voting_data["election_type"] = np.where(
        full_voting_data["Year"].isin(election_years), "presidential", "midterm"
    )

    # convert year column to datetime
    full_voting_data["Year"] = pd.to_datetime(full_voting_data.Year, format="%Y")
    full_voting_data = full_voting_data[
        full_voting_data["Year"] >= datetime(1980, 1, 1)
    ]

    return full_voting_data


voter_data_file_path = os.path.join(
    BASE_PATH, "Raw_Data/voter_turnout_census_bureau.xlsx"
)
full_voting_data_clean = import_clean_voter_data(voter_data_file_path)

# voting data to csv
full_voting_data_clean.to_csv(os.path.join(folderpath, "full_voting_data_clean.csv"),
                              index=False)


# import student enrollment data


def import_clean_student_enrollment_data(file_path):
    enrollment = pd.read_csv(
        os.path.join(file_path, "TrendGenerator.csv"),
        engine="python",
        skiprows=3,
        skipfooter=3,
    )
    years = enrollment["Year"].tolist()
    years = [re.sub(r"\-..", "", y) for y in years]
    years = [datetime.strptime(y, "%Y") for y in years]
    student_enrollment = enrollment["Number of students"].tolist()
    student_enrollment = [s.replace(",", "") for s in student_enrollment]
    student_enrollment = [int(s) for s in student_enrollment]

    student_enroll_df = pd.DataFrame({"years": years, "enrollment": student_enrollment})

    return student_enroll_df


student_enroll_path = os.path.join(BASE_PATH, "Raw_Data")
student_enrollment_df_clean = import_clean_student_enrollment_data(student_enroll_path)

# export enrollment data to csv
student_enrollment_df_clean.to_csv(
    os.path.join(folderpath, "student_enrollment_df_clean.csv"), index=False)
