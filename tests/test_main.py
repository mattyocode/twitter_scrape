import pytest
from unittest import mock

from src.config import API_key, API_secret_key, Access_token, Secret_access_token
from src.main import TwitterAuth, TweepyInitialiser


def test_authenticate():
    output = TwitterAuth.authenticate(API_key, API_secret_key, 
    Access_token, Secret_access_token)
    assert output != None
