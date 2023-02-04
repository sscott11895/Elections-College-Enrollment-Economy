
# Exploring Relationships Between Voter Turnout, College Enrollment, and the Economy

### Authors: Olivia Gunther, Sarah Lueling, & Sarah Scott
### Created Fall 2022 for Data and Programming for Public Policy II - Python Programming Final Project
### Tools/packages used: Github, requests, BeautifulSoup, pandas, numpy, os, re, datetime, pandas_datareader.data, matplotlib, shiny, snscrape.modules.twitter, seaborn, nltk, json, statsmodels.formula.api


Our project idea was inspired by the 2022 midterm elections and the current state of the U.S. economy. 
In summer and fall of 2022, against the backdrop of a looming recession,
many political campaigns focused on Get Out The Vote efforts among college-aged students. 
For our research project, we asked: How do economic measures (specifically GDP,
unemployment rates, and recessions) affect voter turnout rates and student enrollment?
Because of how polarized American politics has become in recent years, we also
factored in the president’s party affiliation to see how this affected outcomes. 

*Note: All images below can be found in the [Figures](https://github.com/sscott11895/Elections-College-Enrollment-Economy/tree/main/Figures) folder.*
*All raw data files are in the folder *Raw Data*.*

### Data Scraping and Cleaning
In order to answer our research question, we used data from a number of different sources: 
 - historic GDP and unemployment rates in the U.S. from 2000-2020, scrapped using the [FRED API](https://fred.stlouisfed.org/) 
 - college student enrollment data, specifically for Title IV institutions, downloaded from
   the National Center for Education Statistics (Dept. of Ed) for 2000-2020.
 - voter turnout and registration data disaggregated by age, downloaded from the [U.S. Census Bureau](https://www.census.gov/data/tables/time-series/demo/voting-and-registration/p20-585.html)
 - basic information on U.S. presidents, including term dates and party affiliation, scrapped using 
   BeautifulSoup from [Wikipedia](https://en.wikipedia.org/wiki/List_of_presidents_of_the_United_States).
 - twitter data from Joe Biden and [Donald Trump](https://www.thetrumparchive.com/)
 
The clean and reshaped versions of these datasets were the foundation of all of our static plots. 
All data manipulation code can be found in the python file [1. Data Scraping and Cleaning.py](https://github.com/sscott11895/Elections-College-Enrollment-Economy/blob/main/1.%20Data%20Scraping%20%26%20Cleaning.py)

### Data Visualizations
Visualizations allowed us to analyze various relationships and trends between 
different combinations of our data. Because we had numerous variables, the biggest
challenge was deciding which combination of metrics would best illustrate the relationships
we were interested in. We ultimately decided to have one static plot that compared GDP to 
unemployment rates. 

![Economic Measures and Recessions, 2000-2020](https://github.com/sscott11895/Elections-College-Enrollment-Economy/blob/main/Figures/Economic%20Measures%20and%20Recessions%2C%202000-2020.png)

Because these were controls for both of our OLS statistical models, we 
wanted to see how they related to each other. We also included recession data in this plot 
to highlight any strange economic happenings during low times. 

Secondly, we looked at college student enrollment data and how this was affected by recessions in another static plot. As 
expected based on economic literature, recessions are associated with higher rates of college 
student enrollment. 

![Student Enrollment and Recessions, 2001-2000](https://github.com/sscott11895/Elections-College-Enrollment-Economy/blob/main/Figures/Student%20Enrollment.png)


Our last two static graphs looked at how voter turnout was affected by the 
presidential party in power, and voter turnout rates vs. unemployment rates.

![How Does the Party in Power Affect Voter Turnout Rates?](https://github.com/sscott11895/Elections-College-Enrollment-Economy/blob/main/Figures/Voter%20Turnout%20and%20Political%20Parties.png)

 
 
![Voter Turnout Vs. Unemployment Rates, 2000-2020](https://github.com/sscott11895/Elections-College-Enrollment-Economy/blob/main/Figures/Voter%20Turnout%20and%20Unemployment%20Rates.png)

These last two plots seek to understand, in a basic way, if there are any noticeable trends in 
those relationships that lend themselves to voting motivations: disagreement with the party in 
power or dissatisfaction with the economy.
	
Our Shiny app offered us a quick interactive approach to look at changes in GDP and unemployment 
rate over time based on recession data and political party data. See a screenshot of this app below. 
If you're interested in exploring the Shiny app, you can read and run the code [2. Plotting.py](https://github.com/sscott11895/Elections-College-Enrollment-Economy/blob/main/2.%20Plotting.py).

![Screenshot of Shiny App](https://github.com/sscott11895/Elections-College-Enrollment-Economy/blob/main/Figures/Shiny%20screenshots/Screen%20Shot%202022-12-01%20at%207.55.27%20PM.png)


We organized our two interactive plots by tabs that focus on recession impacts and political party impacts. 
Within each tab, the user can select the economic measure they want to look at (GDP or unemployment rate), and if 
they wish to display shadowing on the plot. These shadows represent recession dates and 
presidential political parties in their respective tabs. The user is invited to explore the 
data in this way, layer by layer, considering the relationships between the data before diving 
into an OLS model later in the project. We spent time making sure this Shiny app was visually 
appealing and intuitive to a user through its structure and layout.
All data vizualization code is found in the python file [2. Plotting.py](https://github.com/sscott11895/Elections-College-Enrollment-Economy/blob/main/2.%20Plotting.py).


### Twitter Scraping 

To complement our static plots and Shiny website, we focused on data from the most 
recent presidential election in 2020. Specifically, we scraped Twitter data from 
October 2020 for both the Republican presidential candidate, Donald Trump, and from the 
Democratic presidential candidate, Joe Biden, using snscrape. Because the outcome of this election proved 
to be extremely close and because both candidates relied heavily on Twitter data, we wanted 
to use natural language processing to analyze their social media messages in the month leading up 
to the election. The end product was to create visuals that show the top 15 words that each candidate 
used during this time period. 

Note that because in January 2020, Donald Trump was banned from Twitter due to violating their ethics policies. 
We had to use a [different archival website](https://www.thetrumparchive.com/) in order to scrape his tweets from this time period. 

![Word Frequency Distribution for Donald Trump](https://github.com/sscott11895/Elections-College-Enrollment-Economy/blob/main/Figures/Word%20Frequency%20Distribution%20for%20Donald%20Trump.png)


![Word Frequency Distribution for Joe Biden](https://github.com/sscott11895/Elections-College-Enrollment-Economy/blob/main/Figures/Word%20Frequency%20Distribution%20for%20Joe%20Biden.png)


All Twitter Scraping and Visualization code is found in the python file [3. Twitter Word Modeling.py](https://github.com/sscott11895/Elections-College-Enrollment-Economy/blob/main/3.%20Twitter%20Word%20Modeling.py).

### Analysis

We used a basic OLS regression model to predict both voter turnout numbers 
and college student enrollment rates (holding GDP, unemployment rate, and 
the president’s political party constant in both models). For voter turnout numbers, 
our model indicated that an increase in GDP was associated with a statistically significant 
increase in the number of people who vote. Similarly, having a Democratic president in office 
is associated with a statistically significant increase in the voter turnout numbers. 
There was no statistically significant relationship between unemployment rates and voter turnout numbers. 
For student enrollment rates, there were no statistically significant relationships between 
this measure and any of the control variables. 

All Analysis Code can be found in the python file [4. Analysis.py](https://github.com/sscott11895/Elections-College-Enrollment-Economy/blob/main/4.%20Analysis.py).


### Limitations
There were a number of limitations with our model. The first is that our model was 
fitted using very few data points. Due to data quality issues, we chose to only pull 
student enrollment data, GDP and unemployment data, and presidential data from 2000-2020. 
Because election data was only recorded every two years during presidential and midterm elections, 
this drastically limited the number of data points we could use when looking at the relationships 
between our data. Furthermore, an OLS model automatically assumes that there is a linear relationship 
between the independent and dependent variables. This may not be the case for some of these metrics. 
For example, we can imagine that voter turnout rates and GDP have a logarithmic relationship, where 
voter rates initially rise with GDP but then taper out at a certain level of economic development. 
In future iterations of this project, we would focus additional time on data cleaning at the outset
to ensure we have enough data to train a model. 

