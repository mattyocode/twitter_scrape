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

### Mock API
api_mock = MagicMock(spec=tweepy.API)
api_mock.return_value = api_mock

@patch('tweepy.API', api_mock)
def test_get_twitter_client_API():
    response = subject.get_twitter_client_api()
    assert response != None

def get_mock_cursor():
    with open('./src/example_tweet_object.json') as f:
        for line in f:
            tweet = json.loads(line)
            mock_status = MagicMock()
            mock_status.__iter__.return_value = tweet
            mock_cursor = MagicMock()
            mock_cursor.__iter__.return_value = mock_status
    return mock_cursor

@patch.object(Cursor, 'items', return_value=get_mock_cursor())
def test_tweets_from_search_query(mock_cursor):
    subject2 = TwitterClient()
    tweets_list = subject2.tweets_from_search_query('amazing', 1)
    assert tweets_list[0]["id"] == 1312799588156407809
    assert mock_cursor.called

@patch.object(Cursor, 'items', return_value=get_mock_cursor())
def test_tweets_from_user_timeline(mock_cursor):
    subject2 = TwitterClient()
    tweets_list = subject2.tweets_from_user_timeline('amazing', 1)
    assert tweets_list[0]["id"] == 1312799588156407809
    assert mock_cursor.called
