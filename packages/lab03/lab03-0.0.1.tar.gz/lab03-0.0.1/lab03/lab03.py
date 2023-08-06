import re
import pandas as pd
import tweepy
from textblob import TextBlob

##Removes garbage from the text like links and special characters
def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

##Checks the sentiment value
def get_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))

    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

##Compiles a list of sentiment values for every entry in the
##tweet df and adds a new column called 'sentiment'
def add_sentiment(df):
    sentiment = []
    
    for tweet in df['text']:
        curr_sent = get_sentiment(tweet)
        sentiment.append(curr_sent)
    
    df['sentiment'] = sentiment
