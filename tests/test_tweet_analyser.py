from src.tweet_analyser import TweetAnalyser, TweetCleaner

def test_tweet_cleaner():
    tc = TweetCleaner()
    tweet = 'RT @marcobonzanini: just an example! :D http://example.com #NLP'
    expected = ['rt', '@marcobonzanini', ':', 'just', 'an', 'example', '!', ':D', 'http://example.com', '#nlp']
    assert tc.preprocess(tweet) == expected