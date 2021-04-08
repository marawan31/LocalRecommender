from django.shortcuts import render
from django.conf import settings
from pprint import pprint
from .twitter_wrapper import twitter_api

# Create your views here.
def index(request):
    api = twitter_api.TwitterApi()
    tweets = api.get_tweets()
    user_info = api.get_user_info()
    context = {
        'user': user_info,
        'tweets': tweets
    }
    return render(request, 'recommender/index.html', context)