from django.conf import settings
import twitter
import json

class TwitterApi:
    api = twitter.Api(consumer_key=settings.TWITTER_CONFIG['api_key'],
                  consumer_secret=settings.TWITTER_CONFIG['api_secret'],
                  access_token_key=settings.TWITTER_CONFIG['access_token'],
                  access_token_secret=settings.TWITTER_CONFIG['access_token_secret'])

    counts = json.loads(open('countSettings.json').read())
    interest = json.loads(open('interest.json').read())

    def get_user_info(self):
        return self.api.GetUser(screen_name=settings.TWITTER_CONFIG['user_screen_name'])
    
    def get_tweets(self):
        total_tweets =[]
        total_tweets += self.get_tweets_from_feed() + self.get_tweets_from_trends() + self.get_tweets_from_interest() + self.get_tweets_from_people()
        return total_tweets
    
    def get_tweets_from_trends(self):                
        tweetsTrending = []  
        trends = self.api.GetTrendsCurrent()
        for i in trends:
            tweetsTrending += self.api.GetSearch(term=i.name, count=self.counts['countTrends'], lang='en', result_type='popular')
        return tweetsTrending

    def get_tweets_from_feed(self):              
        return self.api.GetHomeTimeline(count=self.counts['countFeed'])

    def get_tweets_from_interest(self):
        tweetsFromInterest = []
        for i in self.interest['interests_subjects']:
            tweetsFromInterest += self.api.GetSearch(term=i, count=self.counts['countInterestsSubjects'], lang='en', result_type='popular')
        return tweetsFromInterest

    def get_tweets_from_people(self):
        tweetsFromPeople = []
        for i in self.interest['interests_accounts']:
            tweetsFromPeople += self.api.GetUserTimeline(screen_name=i, count=self.counts['countInterestsAccounts'], exclude_replies='true')
        return tweetsFromPeople

         
    
