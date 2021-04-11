# LocalRecommender

## Prerequisites

Install python 3.9

## Getting started

Both Windows and Linux are supported

1. First create a virtual envirenment using venv: `python3.9 -m venv localrecommender`
2. Navigate into the env folder `cd localrecommender`
3. Switch to that environment: `souce bin/activate`
4. Install django: `python3.9 -m pip install django`
5. Navigate to a folder you want to place your project in: `cd ...`
6. Clone this repo
7. Run the migrations: `python3.9 manage.py migrate`
8. Start the server: `python3.9 manage.py runserver`
9. Navigate to the url shown in the console



## Contributing

The only two files we will work with at first are `recommender/views.py` where the code to fetch tweets and render them will be contained, and `recommender/templates/index.html` where the html view is contained.

UPDATE:
We now also have `recommender/twipper_wrapper/twitter_api.py` to work on.

to make this work with twitter you need to add `localsettings.json` and it needs to be in this form to load all the twitter api keys and token to use correctly (take those from twitter):

```JSON
{
    "TWITTER_CONFIG":
    {
        "user_screen_name" : "...",
        "api_key" : "...",
        "api_secret": "...",
        "access_token": "...",
        "access_token_secret": "..."
    }
}
```



215 -> 10 par categorie et 5 pour le feed et 5 pour les trends

300 categorie sauvegarder

20 categorie d'interet considere (hashtag et personne)

35 en tweets tous

20 -> poids

5 -> en random des restes des categories

5 -> le feed

5 -> les trends (random sur les 10 des trends)