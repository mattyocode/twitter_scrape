import pytest
import json
from unittest import mock
from mock import patch
import unittest
import tweepy
from tweepy import Cursor

from src.config import API_key, API_secret_key, Access_token, Secret_access_token
from src.main import TwitterAuth, TwitterClient, TwitterStreamer

subject = TwitterClient()

def test_authenticate():
    output = TwitterAuth().authenticate()
    assert output != None

def test_get_twitter_client_API():
    response = subject.get_twitter_client_api()
    assert response != None

# def mocked_get_tweet_object(*args, **kwargs):
#     class MockResponse:
#         def __init__(self, json_data):
#             self.json_data = 

def get_tweet():
    with open('./src/example_tweet_object.json') as f:
        tweet = f.readline()
    print(tweet)
    return tweet

@patch.object(tweepy.API, 'search', return_value=get_tweet())
def test_get_tweets_timeline_to_arr(mock_method):
    subject2 = TwitterClient()
    tweets_list = subject2.get_tweets_from_user_timeline_to_array(count=1, user_id='mattyotweet')
    print(tweets_list)
    tweet = tweets_list[0]
    assert tweet.id == 1312172333109440512