import time
import pandas as pd
import tweepy
from tweepy import API, OAuthHandler

from config import API_key, API_secret_key, Access_token, Secret_access_token

auth = OAuthHandler(API_key, API_secret_key)
auth.set_access_token(Access_token, Secret_access_token)
 
api = tweepy.API(auth)

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

    try:
        # Creation of query method using parameters
        tweets = tweepy.Cursor(api.search,q=text_query).items(count)
        
        # Pulling information from tweets iterable object
        tweets_list = [[tweet.created_at, tweet.id, tweet.text] for tweet in tweets]
        
        # Creation of dataframe from tweets list
        # Add or remove columns as you remove tweet information
        tweets_df = pd.DataFrame(tweets_list)
    
    except BaseException as e:
        print('failed on_status,',str(e))
        time.sleep(3)
    
    return tweets_df

x = tweets_from_search_query('covid', 20)
print(x)