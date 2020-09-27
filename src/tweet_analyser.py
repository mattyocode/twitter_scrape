import pandas as pd
import numpy
import json
import tweepy

from src.main import TwitterAuth, TwitterClient, TwitterStreamer

class TweetAnalyser:
    
    def create_dataframe_from_tweetslist(self, tweets_list):
    # Creation of dataframe from tweets list
    # Add or remove columns as you remove tweet information
    tweets_df = pd.DataFrame(tweets_list)
    return tweets_df