import pytest
from unittest import mock

from src.config import API_key, API_secret_key, Access_token, Secret_access_token
from src.main import TwitterAuth


def test_authenticate():
    output = TwitterAuth().authenticate()
    assert output != None