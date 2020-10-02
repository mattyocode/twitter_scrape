import pandas as pd
import numpy as np
import json
import tweepy
import re
import nltk
from collections import defaultdict
from nltk import bigrams
from nltk.corpus import stopwords
import string
from pprint import pprint
import operator
from collections import Counter
from textblob import TextBlob


class TweetCleaner:
    
    def tokenize(self, s):
        emoticons_str = r"""
        (?:
            [:=;] # Eyes
            [oO\-]? # Nose (optional)
            [D\)\]\(\]/\\OpP] # Mouth
        )"""
    
        regex_str = [
        emoticons_str,
        r'<[^>]+>', # HTML tags
        r'(?:@[\w_]+)', # @-mentions
        r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
        r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
    
        r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
        r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
        r'(?:[\w_]+)', # other words
        r'(?:\S)' # anything else
        ]
        tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
        emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
        return tokens_re.findall(s), tokens_re, emoticon_re
    
    def preprocess(self, s, lowercase=True):
        tokens, tokens_re, emoticon_re = self.tokenize(s)
        if lowercase:
            tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
        return tokens

class TweetAnalyser:

    def __init__(self):
        self.tweet_cleaner = TweetCleaner()

    def clean_tweet(self, tweet):
        return ' '.join(self.tweet_cleaner.preprocess(tweet))
        # return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyse_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1
    
    def create_dataframe_from_tweetslist(self, tweets_list):
        # Creation of dataframe from tweets list
        # Add or remove columns as you remove tweet information
        df = pd.DataFrame(data=[tweet.text for tweet in tweets_list], columns=['tweets_list'])

        df['id'] = np.array([tweet.id for tweet in tweets_list])
        df['user'] = np.array([tweet.user for tweet in tweets_list])
        df['date'] = np.array([tweet.created_at for tweet in tweets_list])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets_list])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets_list])

        return df

    def count_word_frequency_in_tweets(self, filename, keyword):
        stop = self.eliminate_stop_words()
        stop.append(keyword)
        with open(filename) as f:
            count_all = Counter()
            for line in f:
                tweet = json.loads(line)
                # Create a list with all the terms
                terms_stop = [term for term in self.tweet_cleaner.preprocess(tweet['text']) if term not in stop]
                terms_bigrams = bigrams(terms_stop)
                # Update the counter
                count_all.update(terms_stop)
                # Print the first 5 most frequent words
            print(count_all.most_common(10))

    def eliminate_stop_words(self):
        punctuation = list(string.punctuation)
        return stopwords.words('english') + punctuation + ['rt', 'via', '…', 'I', '’', '่', '️', "let's", '🇲', '🇦']

    def term_co_occurances(self, filename):
        stop = self.eliminate_stop_words()
        with open(filename) as f:
            com = defaultdict(lambda : defaultdict(int))
 
            for line in f: 
                tweet = json.loads(line)
                terms_only = [term for term in self.tweet_cleaner.preprocess(tweet['text']) 
                            if term not in stop 
                            and not term.startswith(('#', '@'))]
            
                # Build co-occurrence matrix
                for i in range(len(terms_only)-1):            
                    for j in range(i+1, len(terms_only)):
                        w1, w2 = sorted([terms_only[i], terms_only[j]])                
                        if w1 != w2:
                            com[w1][w2] += 1
            
            com_max = []
            # For each term, look for the most common co-occurrent terms
            for t1 in com:
                t1_max_terms = sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:5]
                for t2, t2_count in t1_max_terms:
                    com_max.append(((t1, t2), t2_count))
            # Get the most frequent co-occurrences
            terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
            print(terms_max[:5])