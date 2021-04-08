from django.conf import settings
import twitter

class TwitterApi:
    api = twitter.Api(consumer_key=settings.TWITTER_CONFIG['api_key'],
                  consumer_secret=settings.TWITTER_CONFIG['api_secret'],
                  access_token_key=settings.TWITTER_CONFIG['access_token'],
                  access_token_secret=settings.TWITTER_CONFIG['access_token_secret'])

    def get_tweets(self):
        #TODO: modify this bad boy
        return self.api.GetSearch(raw_query='q=Soccer&tweet_mode=extended')
    
    def get_user_info(self):
        return self.api.GetUser(screen_name=settings.TWITTER_CONFIG['user_screen_name'])        
    
    def get_trends(self):                  
        return self.api.GetTrendsCurrent()

    #def get_following_tweets(self):      
    #    freinds = self.api.GetFriends(screen_name=settings.TWITTER_CONFIG['user_screen_name'])           
    #    return self.api.GetUserTimeline(screen_name=freinds[0].screen_name, exclude_replies=True, include_rts=False)
         
    
