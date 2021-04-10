from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .twitter_wrapper import twitter_api
from .SubjectExtraction import subject_extraction

from datetime import datetime
from os.path import join

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

@csrf_exempt
def like_post(request):
    user_id = request.POST.get('user_id', '')
    post_id = request.POST.get('post_id', '')
    dt_string = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    with open(join("data", "likes.txt"), "a") as like_file:
        like_file.write(f"{dt_string} {user_id} {post_id}\n")

    sentence = request.POST.get('tweet', '')
    with open(join("data", "interest.txt"), "a") as interest_file:
        interest_file.write(" ".join(subject_extraction.get_topic(sentence)) + "\n")

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