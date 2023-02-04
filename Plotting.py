#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 22:23:52 2022

Code created by: Olivia Gunther, Sarah Lueling, Sarah Scott
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from datetime import datetime
from shiny import App, render, ui

"""
2. Plotting

We create 4 static plots in this section:
    - GDP, unemployment rates, and recession data
    - college student enrollment data and recession data
    - voter turnout rates for presidential and midterm elections, with
    shading to indicate if we had a Republican or Democratic president
    - voter turnout rates for presidential elections vs. unemployment rates

We also include code to create a Shiny app. This allows you to look at GDP
and unemployment rate in relation to both recession data and also
president party data.

"""

BASE_PATH = r'/Users/oliviagunther/Documents/GitHub/final-project-college-enrollment-political-parties'
#BASE_PATH = r"/Users/scotty/Documents/GitHub/final-project-college-enrollment-political-parties"


# import csvs from data wrangling.py file
econ_measures = pd.read_csv(os.path.join(BASE_PATH, "Clean_Data/econ_measures.csv"))
student_enrollment_df_clean = pd.read_csv(
    os.path.join(BASE_PATH, "Clean_Data/student_enrollment_df_clean.csv")
)
full_voting_data_clean = pd.read_csv(
    os.path.join(BASE_PATH, "Clean_Data/full_voting_data_clean.csv")
)
president_df_clean = pd.read_csv(os.path.join(BASE_PATH,
                                              "Clean_Data/president_df_clean.csv"))

# convert all date columns to datetime
econ_measures["DATE"] = pd.to_datetime(econ_measures.DATE)
student_enrollment_df_clean["years"] = pd.to_datetime(student_enrollment_df_clean.years)
full_voting_data_clean["Year"] = pd.to_datetime(full_voting_data_clean.Year)

president_df_clean["Start_Year"] = pd.to_datetime(president_df_clean.Start_Year)
president_df_clean["End_Year"] = pd.to_datetime(president_df_clean.End_Year)



# recessions for axvspan
recessions = [
    (datetime(2001, 1, 1), datetime(2001, 7, 1)),
    (datetime(2007, 10, 1), datetime(2009, 4, 1)),
    (datetime(2020, 1, 1), datetime(2020, 4, 1)),
]

# create list of presidential terms for plotting
president_terms_dates = list(
    zip(
        president_df_clean.Start_Year,
        president_df_clean.End_Year,
        president_df_clean.color,
    )
)


def econ_recessions_plot():
    fig, ax = plt.subplots()
    ax.plot(econ_measures["DATE"], econ_measures["GDP"], color="blue")
    ax.set_ylabel("GDP (in billions of $)", color="blue")
    ax.set_ylim(ymin=0)
    ax2 = ax.twinx()
    ax2.plot(econ_measures["DATE"], econ_measures["UNRATE"], color="green")
    ax2.set_ylabel("Unemployment Rate", color="green")
    ax2.set_ylim(ymin=0)
    for start, end in recessions:
        ax.axvspan(start, end, alpha=0.4, color="red")
    ax.set_title("Economic Measures and Recessions, 2000-2020")
    fig.savefig("Figures/Economic Measures and Recessions, 2000-2020.png")


def student_enrollment_recessions_plot():
    fig, ax = plt.subplots()
    ax.plot(
        student_enrollment_df_clean["years"], student_enrollment_df_clean["enrollment"]
    )
    ax.set_ylabel("Student Enrollment (millions)")
    ax.set_title("College Student Enrollment, 2001-2020")
    for start, end in recessions:
        ax.axvspan(start, end, alpha=0.4, color="red")
    fig.savefig("Figures/Student Enrollment.png")


def voter_turnout_political_party_plot():
    full_voting_data_2020 = full_voting_data_clean[
        full_voting_data_clean["Year"] >= datetime(1999, 1, 1)
    ]

    only_presidential_elections = full_voting_data_2020[
        full_voting_data_2020["election_type"] == "presidential"
    ]
    only_midterm_elections = full_voting_data_2020[
        full_voting_data_2020["election_type"] == "midterm"
    ]

    fig, ax = plt.subplots()
    (line1,) = ax.plot(
        only_presidential_elections["Year"],
        only_presidential_elections["perc_total_voted"],
        color="black",
        label="Pres. Election",
    )
    (line2,) = ax.plot(
        only_midterm_elections["Year"],
        only_midterm_elections["perc_total_voted"],
        linestyle="dotted",
        color="black",
        label="Midterm Election",
    )
    ax.set_ylabel("Voter Turnout (Percent)")
    ax.set_xlabel("Year")
    ax.set_ylim(ymin=0)
    ax.set_title("How Does The Party In Power Affect Voter Turnout Rates?")
    legend_elements = [
        Line2D([0], [0], color="black", lw=2, label="Presidential Elections"),
        Line2D([0], [0], color="black", lw=2, linestyle="dotted",
               label="Midterm Elections"
               ),
        Patch(color="red", label="Republican President"),
        Patch(color="blue", label="Democratic President"),
    ]

    full_legend = ax.legend(
        bbox_to_anchor=(1.04, 1), loc="upper left", handles=legend_elements
    )
    ax.add_artist(full_legend)
    for start, end, color in president_terms_dates:
        ax.axvspan(start, end, alpha=0.3, color=color)
    fig.savefig("Figures/Voter Turnout and Political Parties.png",
                bbox_inches="tight")


def voter_turnout_unemployment_plot():
    full_voting_data_2020 = full_voting_data_clean[
        full_voting_data_clean["Year"] >= datetime(1999, 1, 1)
    ]

    only_presidential_elections = full_voting_data_2020[
        full_voting_data_2020["election_type"] == "presidential"
    ]
    fig, ax = plt.subplots()
    ax.plot(
        only_presidential_elections["Year"],
        only_presidential_elections["perc_total_voted"],
        color="blue",
    )
    ax.set_ylabel("Presidential Voter Turnout (Percent)", color="blue")
    ax.set_xlabel("Year")
    ax.set_ylim(ymin=0)
    ax.set_title("Presidental Voter Turnout Rates vs. Unemployment Rates, 2000 - 2020")
    ax2 = ax.twinx()
    ax2.plot(econ_measures["DATE"], econ_measures["UNRATE"], color="green")
    ax2.set_ylabel("Unemployment Rate (Percent)", color="green")
    ax2.set_ylim(ymin=0)
    fig.savefig("Figures/Voter Turnout and Unemployment Rates.png",
                bbox_inches="tight")


os.chdir(BASE_PATH)
econ_recessions_plot()
student_enrollment_recessions_plot()
voter_turnout_political_party_plot()
voter_turnout_unemployment_plot()


# create shiny app and plots
app_ui = ui.page_fluid(
    ui.row(
        ui.column(
            12,
            ui.h1("Economic Measures, Recessions, and Presidential Political Parties"),
            align="center",
        )
    ),
    ui.row(
        ui.column(
            12,
            ui.h4("Olivia Gunther, Sarah Lueling, Sarah Scott"),
            ui.hr(),
            align="center",
        )
    ),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.p(
                """
                Before writing an OLS model to statistically understand the relationship
                between voter turnout and economic measures like GDP and the unemployment
                rate in the United States, let's explore some visual trends. Take a peek
                at the recession dates and consider how you might've responded during that
                time -- would you have been more or less motivated to vote? How about when
                considering the President's political party? Maybe you'd be more inclined
                to vote when they aren't a member of your preferred party.
                """
            )
        ),
        ui.panel_main(
            ui.navset_tab_card(
                ui.nav(
                    "Recession Impact",
                    ui.input_select(
                        id="econ_measure",
                        label="Choose an economic measure:",
                        choices=["GDP", "Unemployment Rate"],
                    ),
                    ui.input_checkbox(
                        id="recession_shadows", label="Display Recessions"
                    ),
                    ui.output_plot("recession_plot"),
                ),
                ui.nav(
                    "Political Party Impact",
                    ui.input_select(
                        id="econ_measure",
                        label="Choose an economic measure:",
                        choices=["GDP", "Unemployment Rate"],
                    ),
                    ui.input_checkbox(
                        id="party_shadows", label="Display Presidential Party"
                    ),
                    ui.output_plot("party_plot"),
                ),
            )
        ),
    ),
)


def server(input, output, session):
    @output
    @render.plot
    def recession_plot():
        if input.econ_measure() == "GDP":
            if input.recession_shadows() == True:
                fig, ax = plt.subplots()
                ax.plot(econ_measures["DATE"], econ_measures["GDP"], color="blue")
                ax.set_ylabel("GDP (billions of dollars)", color="blue")
                ax.set_ylim(ymin=0)
                for start, end in recessions:
                    ax.axvspan(start, end, alpha=0.4, color="red")
                ax.set_title("GDP and Recessions")
                return ax
            elif input.recession_shadows() == False:
                fig, ax = plt.subplots()
                ax.plot(econ_measures["DATE"], econ_measures["GDP"], color="blue")
                ax.set_ylabel("GDP (billions of dollars)", color="blue")
                ax.set_ylim(ymin=0)
                ax.set_title("GDP")
                return ax
        elif input.econ_measure() == "Unemployment Rate":
            if input.recession_shadows() == True:
                fig, ax = plt.subplots()
                ax.plot(econ_measures["DATE"], econ_measures["UNRATE"], color="green")
                ax.set_ylabel("Unemployment Rate (percent)", color="green")
                ax.set_ylim(ymin=0)
                for start, end in recessions:
                    ax.axvspan(start, end, alpha=0.4, color="red")
                ax.set_title("Unemployment Rate and Recessions")
                return ax
            elif input.recession_shadows() == False:
                fig, ax = plt.subplots()
                ax.plot(econ_measures["DATE"], econ_measures["UNRATE"], color="green")
                ax.set_ylabel("Unemployment Rate (percent)", color="green")
                ax.set_ylim(ymin=0)
                ax.set_title("Unemployment Rate")
                return ax

    @output
    @render.plot
    def party_plot():
        if input.econ_measure() == "GDP":
            if input.party_shadows() == True:
                fig, ax = plt.subplots()
                ax.plot(econ_measures["DATE"], econ_measures["GDP"], color="blue")
                ax.set_ylabel("GDP (billions of dollars)", color="blue")
                ax.set_ylim(ymin=0)
                for start, end, color in president_terms_dates:
                    ax.axvspan(start, end, alpha=0.3, color=color)
                ax.set_title("GDP and Presidential Parties")
                return ax
            elif input.party_shadows() == False:
                fig, ax = plt.subplots()
                ax.plot(econ_measures["DATE"], econ_measures["GDP"], color="blue")
                ax.set_ylabel("GDP (billions of dollars)", color="blue")
                ax.set_ylim(ymin=0)
                ax.set_title("GDP")
                return ax
        elif input.econ_measure() == "Unemployment Rate":
            if input.party_shadows() == True:
                fig, ax = plt.subplots()
                ax.plot(econ_measures["DATE"], econ_measures["UNRATE"], color="green")
                ax.set_ylabel("Unemployment Rate (percent)", color="green")
                ax.set_ylim(ymin=0)
                for start, end, color in president_terms_dates:
                    ax.axvspan(start, end, alpha=0.3, color=color)
                ax.set_title("Unemployment Rate and Presidential Parties")
                return ax
            elif input.party_shadows() == False:
                fig, ax = plt.subplots()
                ax.plot(econ_measures["DATE"], econ_measures["UNRATE"], color="green")
                ax.set_ylim(ymin=0)
                ax.set_ylabel("Unemployment Rate (percent)", color="green")
                ax.set_title("Unemployment Rate")
                return ax


app = App(app_ui, server)
