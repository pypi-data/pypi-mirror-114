"""
This module implements the main functionality of vidstream.
Author: Amit Kumar Kushwaha && Subhankar Saha

"""
import tweepy
import csv 
import os
import re
import time
import nltk
from nltk.corpus import stopwords
from datetime import datetime
from datetime import timezone  
from datetime import date 
import holidays
from textblob import TextBlob
import pandas as pd

parent = os.getcwd()


class tweetScraping:
    """
    Class for the Tweet Scraping.
    Attributes
    ----------
    Private:
        __consumer_key: str
            consumer_key key
        __consumer_secret : str
            consumer_secret key
        __access_token : str
            access_token key
        __access_token_secret : str
            access_token_secret key 
        __file_name : str
            file name 
        __query : str
            which keywords 
        __no_of_tweets : int
            Total tweets no
    Methods
    -------
    Public:
        start : run and scrap
        clean_tweet : Tweet cleaning
        contains_numbers : check number present in tweet or not , return Boolean
        
    """
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, query,file_name = None,no_of_tweets=None ):

        """
        Creates a new instance of Tweet Scraping
        Parameters
        ----------
        __consumer_key: str
            consumer_key key
        __consumer_secret : str
            consumer_secret key
        __access_token : str
            access_token key
        __access_token_secret : str
            access_token_secret key 
        __query : str
            which keywords 
        __file_name : str
            file name (don't give file type, default .csv file) (default = query name)
        __no_of_tweets : int
            Total tweets no (default = 1000)
        """
        nltk.download('stopwords')
        self.__consumer_key = consumer_key
        self.__consumer_secret = consumer_secret
        self.__access_token = access_token
        self.__access_token_secret = access_token_secret
        
        if(len(query)>0 and query[0]!= "#" ):
            self.__query = '#'+query
        else:
            self.__query = query
        if(file_name):
            if(file_name.find('.')!=-1):
                file_name = file_name.split(".")[0]
            self.__file_name = file_name+".csv"
        else:
            qu = self.__query.split("#")[1]
            if(len(qu)==0):
                self.__file_name = self.__query+".csv"
            else:    
                self.__file_name = qu+".csv"
        if(no_of_tweets):
            self.__no_of_tweets = int(no_of_tweets)
        else:
            self.__no_of_tweets = 1000

        print("File Name : "+self.__file_name ,"\nKeyword : " +self.__query,"\nNo of Tweets : " ,self.__no_of_tweets)

    
    def clean_tweet(self,tweet): 
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def contains_numbers(self,tweet):
        return any(char.isdigit() for char in tweet)

    def check_params(self):
        if (self.__consumer_key and self.__consumer_secret and self.__access_token and self.__access_token_secret and self.__query):
            return True
        else:
            return False

    def start(self):
        try:
            if self.check_params():
                # OAuth process, using the keys and tokens
                auth = tweepy.OAuthHandler(self.__consumer_key, self.__consumer_secret)
                auth.set_access_token(self.__access_token, self.__access_token_secret)
                api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
                k=[]
                IN_holidays = holidays.India()
                stop_words = stopwords.words('english')

                if not os.path.isfile(parent+'/'+self.__file_name):
                    tweet_features = pd.DataFrame(columns=[
                        'tweet_id', 'tweet_created_at', 'tweet_created_on_holiday_bool', 
                        'tweet_created_on_weekend_bool','tweet_created_at_noon_bool',
                        'tweet_created_at_eve_bool','user_id','user_screen_name',
                        'user_screen_name_length','user_no_of_tweets',
                        'user_no_of_followers', 'user_no_of_followings',
                        'user_account_age', 'user_no_of_favourites',
                        'user_average_tweets','user_average_favourites',
                        'user_account_location',
                        'tweet_text', 'tweet_text_length', 'tweet_text_optimal_length',
                        'tweet_text_no_of_hashtags', 'tweet_text_contains_hashtags',
                        'tweet_text_contains_url', 'tweet_text_no_of_user_mentions',
                        'tweet_text_contains_user_mentions', 'tweet_text_sentiment',
                        'tweet_text_contains_media', 'tweet_text_contains_number',
                        'tweet_text_contains_upper_words', 'tweet_text_contains_lower_words',
                        'tweet_text_contains_excl', 'tweet_text_contains_retweet_suggestion',
                        'retweeted', 'retweets'
                    ])
                    tweet_features['tweet_id'] = tweet_features['tweet_id'].astype(str)
                    tweet_features.to_csv(parent+'/'+self.__file_name, index=False)                    
                                    
                i=0
                for tweet in tweepy.Cursor(api.search, 
                                    q=self.__query+" -filter:retweets",  
                                    lang="en").items(self.__no_of_tweets):
                    
                    user_id = '~'+tweet.user.id_str+'~'
                    user_screen_name = tweet.user.screen_name
                    user_screen_name_length = len(user_screen_name)
                    user_no_of_tweets = tweet.user.statuses_count
                    user_no_of_followers = tweet.user.followers_count
                    user_no_of_followings = tweet.user.friends_count
                    user_account_age = (datetime.now() - tweet.user.created_at).days
                    user_no_of_favourites = tweet.user.favourites_count
                    try:
                        user_average_tweets = user_no_of_tweets/user_account_age
                    except:
                        user_average_tweets=0
                    try:
                        user_average_favourites = user_no_of_favourites/user_account_age
                    except:
                        user_average_favourites=0
                    user_account_location = tweet.user.location
                    
                    
                    date_parsed = datetime.strptime(tweet._json['created_at'], '%a %b %d %H:%M:%S %z %Y').replace(tzinfo=timezone.utc).astimezone(tz=None).strftime('%Y-%m-%d %H:%M:%S')
                    date = date_parsed.split()[0]
                    hour = int(tweet._json['created_at'].split()[3].split(':')[0])
                    tweet_id = '~'+tweet.id_str+'~'
                    tweet_created_at = tweet._json['created_at']
                    if date in IN_holidays:
                        tweet_created_on_holiday_bool=1
                    else:
                        tweet_created_on_holiday_bool=0
                    if tweet_created_at.split()[0]=='Sun' or tweet_created_at.split()[0]=='Sat':
                        tweet_created_on_weekend_bool=1
                    else:
                        tweet_created_on_weekend_bool=0
                    if hour>=11 and hour<=13:
                        tweet_created_at_noon_bool=1
                    else:
                        tweet_created_at_noon_bool=0
                    if hour>=18 and hour<=21:
                        tweet_created_at_eve_bool=1
                    else:
                        tweet_created_at_eve_bool=0
 
                    clean_tweet_text = self.clean_tweet(tweet.text)
                    analysis = TextBlob(clean_tweet_text)
                    
                    tweet_text = str(tweet.text)
                    tweet_text_length = len(tweet_text)
                    if tweet_text_length>=70 and tweet_text_length<=100:
                        tweet_text_optimal_length=1
                    else:
                        tweet_text_optimal_length=0 
                    try:
                        tweet_text_no_of_hashtags = len(tweet.entities['hashtags'])
                    except:
                        tweet_text_no_of_hashtags=-1
                    if tweet_text_no_of_hashtags>=1:
                        tweet_text_contains_hashtags=1
                    else:
                        tweet_text_contains_hashtags=0
                    try:
                        urls = tweet.entities['urls']
                    except:
                        urls=[]
                    if len(urls)>0:
                        tweet_text_contains_url=1
                    else:
                        tweet_text_contains_url=0
                    try:
                        tweet_text_no_of_user_mentions = len(tweet.entities['user_mentions'])
                    except:
                        tweet_text_no_of_user_mentions = 0
                    if tweet_text_no_of_user_mentions>0:
                        tweet_text_contains_user_mentions=1
                    else:
                        tweet_text_contains_user_mentions=0
                    if analysis.sentiment.polarity>0:
                        tweet_text_sentiment='pos'
                    elif analysis.sentiment.polarity==0:
                        tweet_text_sentiment='nue'
                    else:
                        tweet_text_sentiment='neg'
                    try:
                        medias = tweet.entities['media']
                    except:
                        medias=[]
                    if len(medias)==0:
                        tweet_text_contains_media=0
                    else:
                        tweet_text_contains_media=1
                    if self.contains_numbers(tweet.text):
                        tweet_text_contains_number=1
                    else:
                        tweet_text_contains_number=0
                                                        
                    upper_words=0
                    lower_words=0
                    for clean_word in clean_tweet_text.split():
                        if clean_word.isupper():
                            upper_words+=1
                        if clean_word not in stop_words:
                            if clean_word.islower():
                                lower_words+=1
                    if upper_words>0:
                        tweet_text_contains_upper_words=1
                    else:
                        tweet_text_contains_upper_words=0

                    if lower_words>0:
                        tweet_text_contains_lower_words=1
                    else:
                        tweet_text_contains_lower_words=0
                                                        
                    if '!' in tweet.text:
                        tweet_text_contains_excl = 1
                    else:
                        tweet_text_contains_excl = 0
                                                        
                    tweet_text_contains_retweet_suggestion=0
                    retweet_suggestions = ['RT', 'Pls RT', 'please retweet', 'do RT']
                    for retweet_suggestion in retweet_suggestions:
                        if retweet_suggestion.lower() in tweet.text.lower():
                            tweet_text_contains_retweet_suggestion=1
                    
                    retweets = tweet.retweet_count
                    retweeted = tweet.retweeted
                    
                    
                    
                    tweet_details = [tweet_id, 
                                    tweet_created_at, 
                                    tweet_created_on_holiday_bool,
                                    tweet_created_on_weekend_bool,
                                    tweet_created_at_noon_bool,
                                    tweet_created_at_eve_bool,
                                    user_id, 
                                    user_screen_name,
                                    user_screen_name_length,
                                    user_no_of_tweets,
                                    user_no_of_followers,
                                    user_no_of_followings,
                                    user_account_age,
                                    user_no_of_favourites,
                                    user_average_tweets,
                                    user_average_favourites,
                                    user_account_location,
                                    tweet_text,
                                    tweet_text_length,
                                    tweet_text_optimal_length,
                                    tweet_text_no_of_hashtags,
                                    tweet_text_contains_hashtags,
                                    tweet_text_contains_url,
                                    tweet_text_no_of_user_mentions,
                                    tweet_text_contains_user_mentions,
                                    tweet_text_sentiment,
                                    tweet_text_contains_media,
                                    tweet_text_contains_number,
                                    tweet_text_contains_upper_words,
                                    tweet_text_contains_lower_words,
                                    tweet_text_contains_excl,
                                    tweet_text_contains_retweet_suggestion,
                                    retweeted,
                                    retweets]  

                    tweet_features = pd.DataFrame([tweet_details], columns=[
                        'tweet_id', 'tweet_created_at', 'tweet_created_on_holiday_bool', 
                        'tweet_created_on_weekend_bool','tweet_created_at_noon_bool',
                        'tweet_created_at_eve_bool','user_id','user_screen_name',
                        'user_screen_name_length','user_no_of_tweets',
                        'user_no_of_followers', 'user_no_of_followings',
                        'user_account_age', 'user_no_of_favourites',
                        'user_average_tweets','user_average_favourites',
                        'user_account_location',
                        'tweet_text', 'tweet_text_length', 'tweet_text_optimal_length',
                        'tweet_text_no_of_hashtags', 'tweet_text_contains_hashtags',
                        'tweet_text_contains_url', 'tweet_text_no_of_user_mentions',
                        'tweet_text_contains_user_mentions', 'tweet_text_sentiment',
                        'tweet_text_contains_media', 'tweet_text_contains_number',
                        'tweet_text_contains_upper_words', 'tweet_text_contains_lower_words',
                        'tweet_text_contains_excl', 'tweet_text_contains_retweet_suggestion',
                        'retweeted', 'retweets'
                    ])
                    
                    tweet_features['tweet_id'] = tweet_features['tweet_id'].astype(str)
                    tweet_features.to_csv(parent+'/'+self.__file_name,  mode='a', header=False, index=False)
                    
                    if i%20==0:
                        time.sleep(4)
                    i+=1
                print("Completed Successfully ")
            else:
                print("Please Mandatory Parameter")
        except Exception as e:
            print("Some Error Occurred ")
            print(e)
