import pandas as pd
import numpy as np
import json
import tweepy
import re
from textblob import TextBlob

class TweetCleaner:
    
    def tokenize(self, s):
        emoticons_str = r"""
        (?:
            [:=;] # Eyes
            [oO\-]? # Nose (optional)
            [D\)\]\(\]/\\OpP] # Mouth
        )"""
    
        regex_str = [
        emoticons_str,
        r'<[^>]+>', # HTML tags
        r'(?:@[\w_]+)', # @-mentions
        r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
        r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
    
        r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
        r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
        r'(?:[\w_]+)', # other words
        r'(?:\S)' # anything else
        ]
        tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
        emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
        return tokens_re.findall(s)
    
    def preprocess(self, s, lowercase=False):
        tokens = self.tokenize(s)
        if lowercase:
            tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
        return ' '.join(tokens)

class TweetAnalyser:

    def __init__(self):
        self.tweet_cleaner = TweetCleaner()

    def clean_tweet(self, tweet):
        return self.tweet_cleaner.preprocess(tweet)
        # return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

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