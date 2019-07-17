#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: sonalsannigrahi
"""

import sys 
import tweepy
import json

ACCESS_TOKEN = "your access token"
ACCESS_TOKEN_SECRET = "your secret access token"
CONSUMER_KEY = "your consumer key"
CONSUMER_SECRET = "your secret consumer key"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET) #call_back initialised to None

auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True) #rate limit modified to pass

json_file = open('total_tweets.json', 'w') #Name the json file to download real time tweets into
tweets = [] #initialise list of tweets to empty

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, output_file=sys.stdout): #standard output file
        super(MyStreamListener,self).__init__()
        self.output_file = output_file
        self.api = api
        super(tweepy.StreamListener, self).__init__()
        self.json_file = tweets #initialise
    def on_status(self, status):
        print(status.text, file=self.output_file)
    def on_error(self, status_code):
        #to disconnect upon error
        print(status_code)
        return False
    def on_data(self,tweet):
        self.json_file.append(json.loads(tweet))
        json_file.write(str(tweet)) #writes each into json format of tweets
        


listener = MyStreamListener(output_file=json_file) #creates listener object

stream = tweepy.Stream(auth=api.auth, listener=listener)

try:
    print('Streaming tweets...')
    stream.sample(languages=['en'])
except KeyboardInterrupt:
    print("Keyboard interrupe error!")
finally:
    print('Streaming stopped')
    stream.disconnect()
    json_file.close()
