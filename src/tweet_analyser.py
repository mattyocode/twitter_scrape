import pandas as pd
import numpy as np
import json
import tweepy

class TweetAnalyser:
    
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