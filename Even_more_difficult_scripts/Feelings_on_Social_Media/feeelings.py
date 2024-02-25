# Import necessary libraries
import tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt
from collections import Counter
import re

# Twitter API credentials
consumer_key = 'your-consumer-key'
consumer_secret = 'your-consumer-secret'
access_token = 'your-access-token'
access_token_secret = 'your-access-token-secret'

# Authenticate with the Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Define the search term and the date_since date
search_words = "#climatechange"
date_since = "2018-11-16"

# Collect tweets
tweets = tweepy.Cursor(api.search,
              q=search_words,
              lang="en",
              since=date_since).items(500)

# Create a function to clean the tweets
def clean_tweet(tweet):
    # Remove URLs
    tweet = re.sub(r"http\S+|www\S+|https\S+", '', tweet, flags=re.MULTILINE)
    # Remove user @ references and '#' from tweet
    tweet = re.sub(r'\@\w+|\#','', tweet)
    # Remove emojis
    tweet = tweet.encode('ascii', 'ignore').decode('ascii')
    return tweet

# Create a function to get the polarity
def getAnalysis(text):
    return  TextBlob(text).sentiment.polarity

# Create a function to compute the negative, neutral and positive analysis
def getSentiment(score):
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'

# Collect the sentiment scores for each tweet
sentiments = []
for tweet in tweets:
    cleaned_tweet = clean_tweet(tweet.text)
    analysis = TextBlob(cleaned_tweet)
    sentiments.append(getSentiment(analysis.sentiment.polarity))

# Count the occurrences of each sentiment
sentiment_counts = Counter(sentiments)

# Separate the sentiments and their counts
sentiments = list(sentiment_counts.keys())
counts = list(sentiment_counts.values())

# Create a bar plot of the sentiment counts
plt.bar(sentiments, counts)
plt.title('Sentiment Analysis Results')
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.show()