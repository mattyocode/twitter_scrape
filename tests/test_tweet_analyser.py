from src.tweet_analyser import TweetAnalyser

def test_tweet_cleaner():
    ta = TweetAnalyser()
    tweet = 'RT @marcobonzanini: just an example! :D http://example.com #NLP'
    expected = ['RT', '@marcobonzanini', ':', 'just', 'an', 'example', '!', ':D', 'http://example.com', '#NLP']
    assert ta.clean_tweet(tweet) == expected