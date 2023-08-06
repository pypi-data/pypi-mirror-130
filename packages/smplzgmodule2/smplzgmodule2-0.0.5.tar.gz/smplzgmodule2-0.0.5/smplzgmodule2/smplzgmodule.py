#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
from textblob import TextBlob
import re


# In[20]:


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

def new_data_frame(dataframe):
    new_tweets = pd.DataFrame()
    lst_of_tweet = []

    new_tweets['id'] = dataframe['id']
    
    for line in dataframe['text']:
        x = get_tweet_sentiment(line)
        if x == 'positive':
            lst_of_tweet.append('positive') 
        elif x == 'neutral':
            lst_of_tweet.append('neutral')
        else:
            lst_of_tweet.append('negative')
            
    new_tweets['sentiment'] = lst_of_tweet
    
    return new_tweets.head(30)
        


# In[21]:



# In[ ]:





# In[ ]:




