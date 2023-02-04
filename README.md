# Data and Programming for Public Policy II - Python Programming
# PPHA 30538


## Final Project: Reproducible Research
## Autumn 2022
## Authors: Olivia Gunther, Sarah Lueling, & Sarah Scott
## Final Github Repo Name: final-project-college-enrollment-political-parties

Our project idea was inspired by the recent midterm elections and the current state of the U.S. economy. 
In summer and fall of 2022, against the backdrop of a looming recession,
many political campaigns focused on Get Out The Vote efforts among college-aged students. 
For our research project, we asked: How do economic measures (specifically GDP,
unemployment rates, and recessions) affect voter turnout rates and student enrollment?
Because of how polarized American politics has become in recent years, we also
factored in the president’s party affiliation to see how this affected outcomes. 

In order to answer our research question, we used data from a number of different sources.
We relied heavily on data from the FRED database, pulled using an API, which provided us
with information on historic GDP and unemployment rates in the U.S. from 2000-2020. We 
also imported a csv file with college student enrollment data, specifically for Title IV
institutions from the National Center for Education Statistics (Dept. of Ed) for 2000-2020.
For voter turnout data, we used Census Bureau data that disaggregated voting turnout numbers
by different demographics, which allowed us to focus on college-aged students (18-24 year olds).
Finally, we scraped a simple Wikipedia page listing all the U.S. presidents, their party affiliation,
and their presidential term start and end dates. The clean and reshaped versions of these datasets
were the foundation of all of our static plots. 

Our visualizations allowed us to analyze various relationships and trends between 
different combinations of our data. Because we had numerous variables, the biggest
challenge was deciding which combination of metrics would best illustrate the relationships
we were interested in. We ultimately decided to have one static plot that compared GDP to 
unemployment rates. Because these were controls for both of our OLS statistical models, we 
wanted to see how they related to each other. We also included recession data in this plot 
to highlight any strange economic happenings during low times. Secondly, we looked at college 
student enrollment data and how this was affected by recessions in another static plot. As 
expected based on economic literature, recessions are associated with higher rates of college 
student enrollment. Our third static graph looked at how voter turnout was affected by the 
presidential party in power. Lastly, we looked at voter turnout rates vs. unemployment rates. 
These last two plots seek to understand, in a basic way, if there are any noticeable trends in 
those relationships that lend themselves to voting motivations: disagreement with the party in 
power or dissatisfaction with the economy.
	
Our Shiny app offered us a quick interactive approach to look at changes in GDP and unemployment 
rate over time based on recession data and political party data. We organized our two interactive 
plots by tabs that focus on recession impacts and political party impacts. Within each tab, the 
user can select the economic measure they want to look at (GDP or unemployment rate), and if 
they wish to display shadowing on the plot. These shadows represent recession dates and 
presidential political parties in their respective tabs. The user is invited to explore the 
data in this way, layer by layer, considering the relationships between the data before diving 
into an OLS model later in the project. We spent time making sure this Shiny app was visually 
appealing and intuitive to a user through its structure and layout.

To complement our static plots and Shiny website, we focused on data from the most 
recent presidential election in 2020. Specifically, we scraped Twitter data from 
October 2020 for both the Republican presidential candidate, Donald Trump, and from the 
Democratic presidential candidate, Joe Biden. Because the outcome of this election proved 
to be extremely close and because both candidates relied heavily on Twitter data, we wanted 
to use natural language processing to analyze their social media messages in the month leading up 
to the election. The end product was to create visuals that show the top 15 words that each candidate 
used during this time period. 

We ran into three major challenges during the text processing section. One was figuring 
out a way to scrape Twitter data. Because Twitter sells their data, they rarely allow 
people to scrape unlimited information from their site. As such, different packages have 
been developed to address this issue. We specifically used the package “snscrape”. Another 
challenge was the inability to scrape Donald Trump's Twitter data. In January 2020, Donald Trump 
was banned from Twitter due to violating their ethics policies. We had to use a different archival 
website in order to scrape his tweets from this time period. In addition, preprocessing the text 
required a lot of work. In this case, it matters which order the cleaning is performed in, 
i.e. cleaning symbols before cleaning URLs will result in faulty results. 
After a lot of experimenting, it worked out well in the end.

We used a basic OLS regression model to predict both voter turnout numbers 
and college student enrollment rates (holding GDP, unemployment rate, and 
the president’s political party constant in both models). For voter turnout numbers, 
our model indicated that an increase in GDP was associated with a statistically significant 
increase in the number of people who vote. Similarly, having a Democratic president in office 
is associated with a statistically significant increase in the voter turnout numbers. 
There was no statistically significant relationship between unemployment rates and voter turnout numbers. 
For student enrollment rates, there were no statistically significant relationships between 
this measure and any of the control variables. 

There were a number of limitations with our model. The first is that our model was 
fitted using very few data points. Due to data quality issues, we chose to only pull 
student enrollment data, GDP and unemployment data, and presidential data from 2000-2020. 
Because election data was only recorded every two years during presidential and midterm elections, 
this drastically limited the number of data points we could use when looking at the relationships 
between our data. Furthermore, an OLS model automatically assumes that there is a linear relationship 
between the independent and dependent variables. This may not be the case for some of these metrics. 
For example, we can imagine that voter turnout rates and GDP have a logarithmic relationship, where 
voter rates initially rise with GDP but then taper out at a certain level of economic development. 
In the future, making sure to  longevity of the model is very important. 


