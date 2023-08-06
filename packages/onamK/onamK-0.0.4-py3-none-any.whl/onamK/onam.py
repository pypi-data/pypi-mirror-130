import re
import tweepy
import pandas as pd
from tweepy import OAuthHandler
from textblob import TextBlob

def update_progress(progress):
    if progress == 1:
        print("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(progress * 50), progress*100), flush=True)
    else :
        print("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(progress * 50), progress*100), end="", flush=True)

def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def get_tweet_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

def answer_function(df):
    sentiment = []
    for i in range(len(df)):
        sentiment.append(get_tweet_sentiment(df['text'][i]))
        update_progress(i/len(df))
    update_progress(1)
    df['Sentiment'] = sentiment
    df.to_csv('data.csv',index=False)
    return df
