from django.conf import settings
import twitter
import json
import random
from datetime import datetime

class TwitterApi:
    api = twitter.Api(consumer_key=settings.TWITTER_CONFIG['api_key'],
                  consumer_secret=settings.TWITTER_CONFIG['api_secret'],
                  access_token_key=settings.TWITTER_CONFIG['access_token'],
                  access_token_secret=settings.TWITTER_CONFIG['access_token_secret'])

    counts = json.loads(open('countSettings.json').read())

    def get_user_info(self):
        return self.api.GetUser(screen_name=settings.TWITTER_CONFIG['user_screen_name'])
    
    def get_tweets(self):
        tweets_interests = []
        with open("interest.json") as f:
                properties = json.loads(f.read())
                if (properties['interests'] is not None):
                    interests = properties['interests'] 
                    def sortFunc(element):
                        return element['weight']
                    interests.sort(key=sortFunc, reverse=True)
                    interests = interests[:self.counts['countSubjects']]
                    for interest in interests:
                        if (interest['element'].startswith('@')):
                            some_tweets = self.get_tweets_from_person(interest["element"][1:])
                            tweets_interests.append({'weight': interest['weight'], 'interest': interest['element'], 'tweets': some_tweets})
                        else:
                            some_tweets = self.get_tweets_from_interest(interest["element"])
                            tweets_interests.append({'weight': interest['weight'], 'interest': interest['element'], 'tweets': some_tweets})

        # Maybe we can have a better way later using this normalization, but for now we get 1 tweet per interest 
        #tweets_interests.sort(key=sortFunc, reverse=True)
        #tweets_interests

        #count = elf.counts['countSubjects']
        #element_n = count * 2
        #tweet_count = round((math.sqrt((4*element_n) + 1) - 1)/2)
            
        total_tweets = []

        for interest_tweets in tweets_interests:
            if(len(interest_tweets['tweets']) > 0):
                total_tweets.append(interest_tweets['tweets'][0])

        count_trends = self.counts['countTrends']
        count_feed = self.counts['countFeed']
        remaining_count = self.counts['countSubjects'] - len(total_tweets)
        if(remaining_count > 0):
            count_trends += int(remaining_count /2)
            count_feed += int(remaining_count /2)
        total_tweets += self.get_tweets_from_feed(count_feed) + self.get_tweets_from_trends(count_trends)
        unique = {}
        for elem in total_tweets:
            if elem.id not in unique.keys():
                unique[elem.id] = elem
        tweets = list(unique.values())
        
        tweets.sort(key=lambda r: datetime.strptime(r.created_at, "%a %b %d %H:%M:%S %z %Y"), reverse=True)
        return tweets
    
    def get_tweets_from_trends(self, tweet_count):                
        tweetsTrending = []  
        trends = self.api.GetTrendsCurrent()
        for trend in random.sample(trends, tweet_count):
            tweets = self.api.GetSearch(raw_query="q=" + trend.query +"%20-filter%3Areplies%20-filter%3Aretweets&tweet_mode=extended&count=1&lang=en", count=1, lang='en', result_type='popular')
            tweetsTrending += tweets
        return tweetsTrending

    def get_tweets_from_feed(self, tweet_count):              
        some_tweets = self.api.GetHomeTimeline(count=tweet_count, exclude_replies=True)
        return some_tweets

    def get_tweets_from_person(self, user_screen_name):
        tweets = self.api.GetSearch(raw_query="q=from%3A"+ user_screen_name +"%20-filter%3Areplies%20-filter%3Aretweets&tweet_mode=extended&count=11", count=10, lang='en', result_type='popular')
        return tweets

    def get_tweets_from_interest(self, interest):
        tweets = self.api.GetSearch(raw_query="q=%23"+ interest +"%20-filter%3Areplies%20-filter%3Aretweets&tweet_mode=extended&count=11&lang=en", count=10, lang='en', result_type='popular')
        return tweets

         
    
