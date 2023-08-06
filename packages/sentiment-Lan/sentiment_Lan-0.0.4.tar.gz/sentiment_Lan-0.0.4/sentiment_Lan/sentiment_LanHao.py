from nltk.util import pr
import pandas as pd
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


def clean_tweet(tweet):
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

def add_sentiment(dataframe):
    sentimentCol=[] 
    for line in range(len(dataframe)):
        sentimentCol.append(get_tweet_sentiment(dataframe['text'][line])) 
        #access only the txt column, involve 'text', so it only fits our assignment file 

    newData= pd.DataFrame() 
    # newData = data.csv + sentiment column
    newData = dataframe
    newData['sentiment'] = sentimentCol
    print(newData.head(30))

def main():
    df_csv = pd.read_csv('data.csv') 
    # the csv file name's been changed to data
    add_sentiment(df_csv)
    
if __name__ == '__main__':
    main()
