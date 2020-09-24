import tweepy
from tweepy import OAuthHandler

from config import API_key, API_secret_key, Access_token, Secret_access_token
 
auth = OAuthHandler(API_key, API_secret_key)
auth.set_access_token(Access_token, Secret_access_token)
 
api = tweepy.API(auth)
print(api)