import time
import pandas as pd
import numpy
import json
import tweepy
from matplotlib import pyplot as plt
import numpy as np
from tweepy import API, OAuthHandler, Cursor, Stream
from tweepy.streaming import StreamListener

from config import API_key, API_secret_key, Access_token, Secret_access_token
from tweet_analyser import TweetAnalyser
from data_visualiser import DataVisualiser

class TwitterAuth:

    def authenticate(self):
        auth = OAuthHandler(API_key, API_secret_key)
        auth.set_access_token(Access_token, Secret_access_token)
        return auth

class TwitterClient:

    def __init__(self, user=None, filename=None):
        self.auth = TwitterAuth().authenticate()
        self.twitter_client = API(self.auth)
        self.twitter_user = user
        self.json_file = filename

    def get_twitter_client_api(self):
        return self.twitter_client

    def tweets_from_user_timeline(self, count, user_id):
        tweets_list = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=user_id).items(count):
            if self.tweet_filtering_criteria(tweet):
                tweets_list.append(tweet)
                self.store_as_json(tweet._json)

        return tweets_list

    def tweets_from_search_query(self, text_query, count):
        tweets_list = []
        try:
            for tweet in Cursor(self.twitter_client.search,q=text_query,
                lang='en',wait_on_rate_limit=True).items(count):
                if self.tweet_filtering_criteria(tweet):
                    tweets_list.append(tweet)
                    self.store_as_json(tweet._json)
        
        except BaseException as e:
            print('failed on_status:',str(e))
            time.sleep(3)
        
        return tweets_list

    def tweet_filtering_criteria(self, tweet):
        try:
            if not tweet.retweeted and 'RT @' not in tweet.text:
                return True
        except:
            pass
        

    def store_as_json(self, tweet):
        with open(self.json_file, 'a+') as f:
            f.write(json.dumps(tweet))
            f.write('\n')

    def prettify_json(filename):
        with open(filename, 'r') as f:
            line = f.readline() # read only the first tweet/line
            tweet = json.loads(line) # load it as Python dict
            print(json.dump(tweet, indent=4)) # pretty-print

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

    twitter_client = TwitterClient(filename="test_store.json")
    tweet_analyser = TweetAnalyser()
    data_visualiser = DataVisualiser()

    api = twitter_client.get_twitter_client_api()

    tweets_list = twitter_client.tweets_from_search_query('amazing', 10)

    # df = tweet_analyser.create_dataframe_from_tweetslist(tweets_list)
    # df['sentiment'] = np.array([tweet_analyser.analyse_sentiment(tweet) for tweet in df['tweets_list']])

    # print(df.head(20))

    tweet_analyser.term_co_occurances('test_store.json')
    x = tweet_analyser.count_word_frequency_in_tweets('test_store.json', 'streaming')
    print(x)
