from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        'range': range(3)
    }
    return render(request, 'recommender/index.html', context)