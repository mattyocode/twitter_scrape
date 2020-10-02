import vincent
from tweet_analyser import TweetAnalyser

class DataVisualiser:

    def __init__(self, tweet_analyser=TweetAnalyser()):
        self.tweet_analyser = tweet_analyser

    def bar_graph_term_frequency(self, word_freq, output_file):
        pass



#Likes over time using pd.Series
# time_of_likes = pd.Series(data=df['likes'].values, index=df['date'])
# time_of_likes.plot(figsize=(16,4), color='g')
# plt.show()