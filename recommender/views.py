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
    post_id = request.POST.get('post_id', '')
    sentence = request.POST.get('tweet', '')
    interests = []
    new_interests = []
    hash_tags = subject_extraction.get_hashtags(sentence)    
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
    post_id = request.POST.get('post_id', '')
    with open(join("data", "likes.txt"), "r") as f:
        lines = f.readlines()
    with open(join("data", "likes.txt"), "w") as f:
        for line in lines:
            if line.split(" ")[2].strip() != post_id:
                f.write(line)

    return HttpResponse(200)