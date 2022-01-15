import tweepy
from textblob import TextBlob
import preprocessor as p
import statistics
from typing import List
from secret import api_key, api_key_secret, bearer_token 

auth = tweepy.AppAuthHandler(api_key, api_key_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

def get_tweets(keyword):
    all_tweets = []
    for tweet in tweepy.Cursor(api.search_tweets, q=keyword, tweet_mode='extended', lang='en').items(10):
        all_tweets.append(tweet.full_text)
    return all_tweets

def clean_tweets(all_tweets):
    tweets_clean = []
    for tweet in all_tweets:
        tweets_clean.append(p.clean(tweet))
    return tweets_clean

def get_popularity(all_tweets):
    scores = []
    for tweet in all_tweets:
        blob = TextBlob(tweet)
        scores.append(blob.sentiment.polarity)
    return scores

def generate_score(keyword):
    tweets = get_tweets(keyword)
    tweets_clean = clean_tweets(tweets)
    sentiment_scores = get_popularity(tweets_clean)

    average_score = statistics.mean(sentiment_scores)
    return average_score


if __name__ == "__main__":
    print("Compare the Twitter popularity of two keywords. 1:")
    first_thing = input()
    print("2:")
    second_thing = input()
    print('\n')
    first_score = generate_score(first_thing)
    second_score = generate_score(second_thing)

    if first_score > second_score:
        print (f"{first_thing} is more popular than {second_thing}")