import pytest
import json
from unittest import mock
from mock import patch, Mock, MagicMock
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

def get_mock_cursor():
    with open('./src/example_tweet_object.json') as f:
        for line in f:
            tweet = json.loads(line)
            mock_cursor = MagicMock()
            mock_cursor.__iter__.return_value = tweet
            mock_cursor.tweet._json.return_value = json.dumps(tweet)
    return mock_cursor

@patch.object(Cursor, 'items', return_value=get_mock_cursor())
def test_tweets_from_search_query(mock_cursor):
    subject2 = TwitterClient()
    tweets_list = subject2.tweets_from_search_query('amazing', 1)
    assert tweets_list[0]["id"] == 1312799588156407809

# mock_cursor = Mock(Cursor)
# mock_cursor.return_value.json.return_value = get_tweet()

# @patch('src.main.Cursor')
# def test_tweets_from_search_query(mock_cursor):


# TODO create mock cursor with patched api that sends get_tweet
# def mock_cursor():


# @patch.object(tweepy.API, 'get_status', return_value=get_tweet())
# def test_get_tweets_timeline_to_arr(mock_method):
#     subject2 = TwitterClient()
#     tweets_list = subject2.get_tweets_from_user_timeline_to_array(count=1, user_id=None)
#     tweet = tweets_list[0]
#     assert tweet.id == 1312172333109440512