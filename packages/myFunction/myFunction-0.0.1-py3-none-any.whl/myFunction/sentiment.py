import re
import pandas as pd
from textblob import TextBlob
import numpy as np


def calculate_Sentiment(df):
    def clean_tweet( tweet):
       
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
  

    def get_tweet_sentiment( tweet):
        # create TextBlob object of passed tweet text
        analysis = TextBlob(clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
    
    
    df['Sentiment'] = df.apply(lambda a: get_tweet_sentiment(a['text']), axis=1)
    return df.head(30)