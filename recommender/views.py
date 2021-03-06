from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .twitter_wrapper import twitter_api
from .SubjectExtraction import subject_extraction

from datetime import datetime
from os.path import join
import json

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

def contains(list, filter):
    for x in list:
        if filter(x):
            return True
    return False

@csrf_exempt
def like_post(request):
    user_id = "@" + request.POST.get('user_id', '')
    sentence = request.POST.get('tweet', '')
    interests = []
    new_interests = []
    hash_tags = subject_extraction.get_hashtags(sentence) #+ subject_extraction.get_topics(sentence)
    #subjects = subject_extraction.get_topics(sentence)
    with open("interest.json") as f:
        properties = json.loads(f.read())
        if properties is not None:
            interests = properties['interests']
    set_user = False
    for x in interests:
        if x['element'] == user_id:
            x['weight'] += 0.1
            set_user = True
            break
    if(not set_user):
        new_interests.append({'element': user_id, 'weight': 0.1})

    for index, interest in enumerate(interests):
        if (interest in hash_tags):
            hash_tags.remove(interest)
            interests[index] += 0.1

    for hash_tag in hash_tags:
        new_interests.append({'element': hash_tag, 'weight': 0.1})
    interests.sort(key=lambda e: e['weight'], reverse=True)
    interests = interests[:(300-len(new_interests))] + new_interests
    with open('interest.json', 'w') as outfile:
        json.dump({'interests': interests}, outfile)

    return HttpResponse(200)

@csrf_exempt
def unlike_post(request):
    user_id = "@" + request.POST.get('user_id', '')
    interests = []
    set_user = False
    with open("interest.json") as f:
        properties = json.loads(f.read())
        if properties is not None:
            interests = properties['interests']
            for x in interests:
                if x['element'] == user_id:
                    x['weight'] -= 0.1
                    set_user = True
                    break
    if(set_user):
        with open('interest.json', 'w') as outfile:
            json.dump({'interests': interests}, outfile)

    return HttpResponse(200)