import time
import pandas as pd
import numpy
import json
import tweepy
from matplotlib import pyplot as plt
import numpy as np
from tweepy import API, OAuthHandler, Cursor
from tweepy import Stream
from tweepy.streaming import StreamListener

from config import API_key, API_secret_key, Access_token, Secret_access_token
from tweet_analyser import TweetAnalyser

class TwitterAuth:

    def authenticate(self):
        auth = OAuthHandler(API_key, API_secret_key)
        auth.set_access_token(Access_token, Secret_access_token)
        return auth

# class TweepyInitialiser:

#     def initialize_tweepy_api(self):
#         auth = TwitterAuth().authenticate()
#         api = tweepy.API(auth)
#         return api

class TwitterClient:

    def __init__(self, user=None):
        self.auth = TwitterAuth().authenticate()
        self.twitter_client = API(self.auth)
        self.twitter_user = user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_tweets_from_user_timeline_to_array(self, count):
        tweets_list = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(count):
            if not tweet.retweeted and 'RT @' not in tweet.text:
                tweets_list.append(tweet)

        return tweets_list

    def get_tweets_from_user_timeline_to_json(self, count):
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(count):
            self.process_or_store(tweet._json)

    def tweets_from_search_query(self, text_query, count):
        #Most recent tweets containing text_query keyword
        try:
            # Creation of query method using parameters
            tweets = tweepy.Cursor(api.search,q=text_query).items(count)
            
            # Pulling information from tweets iterable object
            tweets_list = [[tweet.created_at, tweet.text, tweet.user, 
            tweet.favorite_count] for tweet in tweets]
        
        except BaseException as e:
            print('failed on_status,',str(e))
            time.sleep(3)
        
        return tweets_list

    def process_or_store(tweet):
        print(json.dumps(tweet))

    def prettify_json(filename):
        with open(filename, 'r') as f:
            line = f.readline() # read only the first tweet/line
            tweet = json.loads(line) # load it as Python dict
            print(json.dumps(tweet, indent=4)) # pretty-print

class TwitterStreamer:

    def __init__(self):
        self.twitter_auth = TwitterAuth()

    def stream_tweets(self, scaped_to_filename, query_list):
        api = TweepyInitialiser.initialize_tweepy_api()   
        listener = MyListener()

        stream = Stream(auth, listener)
        stream.filter(track=query_list)

class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            with open('python.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        if status == 420:
            #Return false if rate limit reached.
            return False
        print(status)
        return True



if __name__ == '__main__':

    twitter_client = TwitterClient("mrjamesob")
    tweet_analyser = TweetAnalyser()

    api = twitter_client.get_twitter_client_api()

    tweets_list = twitter_client.get_tweets_from_user_timeline_to_array(20)

    # tweets_list = api.user_timeline(screen_name="mrjamesob", count=200)

    df = tweet_analyser.create_dataframe_from_tweetslist(tweets_list)
    df['sentiment'] = np.array([tweet_analyser.analyse_sentiment(tweet) for tweet in df['tweets_list']])

    print(df.head(10))

    # print(np.max(df['likes']))

    #Likes over time using pd.Series
    # time_of_likes = pd.Series(data=df['likes'].values, index=df['date'])
    # time_of_likes.plot(figsize=(16,4), color='g')
    # plt.show()

#    print(dir(tweet_list[0]))

# twitter_client = TwitterClient('barackobama')
# print(twitter_client.get_tweets_from_user_timeline(1))

