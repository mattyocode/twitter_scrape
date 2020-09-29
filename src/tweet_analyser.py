import pandas as pd
import numpy as np
import json
import tweepy
import re
from textblob import TextBlob


class TweetAnalyser:

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyse_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1
    
    def create_dataframe_from_tweetslist(self, tweets_list):
        # Creation of dataframe from tweets list
        # Add or remove columns as you remove tweet information
        df = pd.DataFrame(data=[tweet.text for tweet in tweets_list], columns=['tweets_list'])

        df['id'] = np.array([tweet.id for tweet in tweets_list])
        df['user'] = np.array([tweet.user for tweet in tweets_list])
        df['date'] = np.array([tweet.created_at for tweet in tweets_list])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets_list])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets_list])


        return df