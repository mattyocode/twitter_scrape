import time
import pandas as pd
import tweepy
import json
from tweepy import API, OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

from config import API_key, API_secret_key, Access_token, Secret_access_token

def authenticate(API_key, API_secret_key, Access_token, Secret_access_token):
    auth = OAuthHandler(API_key, API_secret_key)
    auth.set_access_token(Access_token, Secret_access_token)
    return auth

def initialize_tweepy_api():
    auth = authenticate(API_key, API_secret_key, Access_token, Secret_access_token)
    api = tweepy.API(auth)
    return api

def tweets_from_user(username, count):

    try:     
        # Creation of query method using parameters
        tweets = tweepy.Cursor(api.user_timeline,id=username).items(count)

        # Pulling information from tweets iterable object
        tweets_list = [[tweet.created_at, tweet.id, tweet.text] for tweet in tweets]

        # Creation of dataframe from tweets list
        # Add or remove columns as you remove tweet information
        tweets_df = pd.DataFrame(tweets_list)
    except BaseException as e:
        print('failed on_status,',str(e))
        time.sleep(3)

    return tweets_df

def tweets_from_search_query(text_query, count):
    #Most recent tweets containing text_query keyword
    api = initialize_tweepy_api()
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

def create_dataframe_from_tweetslist(tweets_list):
    # Creation of dataframe from tweets list
    # Add or remove columns as you remove tweet information
    tweets_df = pd.DataFrame(tweets_list)
    return tweets_df

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
        print(status)
        return True
 
# twitter_stream = Stream(auth, MyListener())
# twitter_stream.filter(track=['#python'])

def prettify_json(filename):
    with open(filename, 'r') as f:
        line = f.readline() # read only the first tweet/line
        tweet = json.loads(line) # load it as Python dict
        print(json.dumps(tweet, indent=4)) # pretty-print

x = create_dataframe_from_tweetslist(tweets_from_search_query('work', 20))
print(x)