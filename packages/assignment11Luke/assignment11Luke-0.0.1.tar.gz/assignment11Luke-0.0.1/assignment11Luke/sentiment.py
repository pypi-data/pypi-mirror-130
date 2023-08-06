import re
from textblob import TextBlob
import pandas as pd


def clean_tweet(tweet):
    '''
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
  
def get_tweet_sentiment(tweet):
    '''
    Utility function to classify sentiment of passed tweet
    using textblob's sentiment method
    '''
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'


tweets = pd.read_csv('vaccination_tweets.csv')
sentimentList = []
for line in tweets['text']:
    sentimentList.append(get_tweet_sentiment(clean_tweet(line)))
sentimentVals = pd.Series(sentimentList, name = 'Sentiment')
newTweets = pd.concat([tweets, sentimentVals], axis = 1)

print(newTweets['Sentiment'].head(30))