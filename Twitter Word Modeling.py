#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 22:23:52 2022

Code created by: Olivia Gunther, Sarah Lueling, Sarah Scott
"""

import pandas as pd
import os
import re
import matplotlib.pyplot as plt
import snscrape.modules.twitter as sntwitter
import seaborn as sns
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import collections
import string
from nltk import word_tokenize
import json


'''
3. Text Processing and Word Frequency Diagram

Below, we scrape Donald Trump and Joe Biden's Twitter data from October 2020 in
the runup to the 2020 presidential election. We then identified the most common
words used by these candidates.
'''

# Get Archived Tweets
BASE_PATH = r'/Users/oliviagunther/Documents/GitHub/final-project-college-enrollment-political-parties'
#BASE_PATH = r'/Users/scotty/Documents/GitHub/final-project-college-enrollment-political-parties'


path_creation = os.path.join(BASE_PATH, "Raw_Data/trump_tweets.json")
with open(path_creation) as json_file:
    data = json.load(json_file)

trump_twitter = pd.DataFrame(data)
trump_twitter = trump_twitter.rename(columns={"text": "Content"})

# trump tweets to csv
folderpath = os.path.join(BASE_PATH, "Clean_Data")
trump_twitter.to_csv(os.path.join(folderpath, "trump_twitter.csv"))

# Get Tweets


def get_twitter_data(username, start_date, end_date):
    tweets_list1 = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'from:{username} since:{start_date} until:{end_date}').get_items()):
        tweets_list1.append([tweet.date,
                             tweet.content,
                             tweet.user.username])

    tweets_df = pd.DataFrame(tweets_list1, columns=["Date Created",
                                                    "Content", "User"])
    return tweets_df


def content_string(df):
    return ' '.join(df["Content"])


our_friend_joe = get_twitter_data("JoeBiden", "2020-10-01", "2020-10-31")

# biden tweets to csv
our_friend_joe.to_csv(os.path.join(folderpath, "our_friend_joe.csv"))


joe_string = content_string(our_friend_joe)
trump_string = content_string(trump_twitter)

# Cleaning Steps and then creating graph with top words dictionary
nltk.download("stopwords")
words_to_clean = stopwords.words("english")
words_to_clean += ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
words_to_clean += list(string.punctuation)


def remove_links(df):
    return re.sub(r'http\S+', '', df)


def tokenize_lowercase(text):
    tokens = word_tokenize(text)
    tokenlist = [token.lower() for token in tokens if token.lower() not in words_to_clean]
    return tokenlist


def remove_numbers(t_object):
    numberless = list(filter(lambda x: x.isalpha(), t_object))
    return numberless


lemmatizer = WordNetLemmatizer()


def lemmatize_txt(df_text):
    lemmatized = []
    for w in df_text:
        lemmatized.append(lemmatizer.lemmatize(w))
    return lemmatized


def dict_20(df):
    resulting_count = collections.Counter(df)
    value_key_pairs = ((value, key) for (key, value) in resulting_count.items())
    sorted_value_key_pairs = sorted(value_key_pairs, reverse=True)
    common_words = {k: v for v, k in sorted_value_key_pairs}
    return dict(sorted(common_words.items(), key=lambda x: x[1], reverse=True)[:20])


def key_words(df, title):
    keysList = list(df.keys())
    ValueList = list(df.values())
    plt.figure(figsize=(15, 8))
    sns.barplot(x=keysList, y=ValueList)
    plt.title(f'Word Frequency Distribution for {title}', fontsize=18)
    plt.xlabel("Frequency", fontsize=12)
    plt.ylabel("Words", fontsize=12)
    plt.savefig(f'Figures/Word Frequency Distribution for {title}.png',
                bbox_inches="tight")


lower_joe_string = remove_links(joe_string)
lower_trump_string = remove_links(trump_string)

joe_tokenized = tokenize_lowercase(lower_joe_string)
trump_tokenized = tokenize_lowercase(lower_trump_string)

joe_remove_nums = remove_numbers(joe_tokenized)
trump_remove_nums = remove_numbers(trump_tokenized)

joe_lemmatize_text = lemmatize_txt(joe_remove_nums)
trump_lemmatize_text = lemmatize_txt(trump_remove_nums)

joe_dict_20 = dict_20(joe_lemmatize_text)
trump_dict_20 = dict_20(trump_lemmatize_text)

biden_keywords = key_words(joe_dict_20, "Joe Biden")
trump_keywords = key_words(trump_dict_20, "Donald Trump")
