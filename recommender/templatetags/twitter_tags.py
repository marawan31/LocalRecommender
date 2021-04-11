from django import template

register = template.Library()

image_html = '<img src="{url}" style="text-align: center;display: block; width:70%; margin:1rem 2rem 0rem 0rem;">'
video_html = '<video preload="none" playsinline="" aria-label="Embedded video" disablepictureinpicture="" poster="{image_url}" src="{url}" style="background-color: black; top: 0%; left: 0%; transform: rotate(0deg) scale(1.005);width:60%" controls></video>'

@register.filter()
def twitter_date(value):
    import datetime
    split_date = value.split()
    del split_date[0], split_date[-2]
    value = ' '.join(split_date)  # Fri Nov 07 17:57:59 +0000 2014 is the format
    return datetime.datetime.strptime(value, '%b %d %H:%M:%S %Y')

@register.filter()
def urlize_tweet_text(tweet):
    """ Turn #hashtag and @username in status text to Twitter hyperlinks,
        similar to the ``urlize()`` function in Django.
    """
    try:
        from urllib import quote
    except ImportError:
        from urllib.parse import quote
    hashtag_url = '<span class="text-blue-400"> <a href="https://twitter.com/search?q=%%23%s" target="_blank">#%s</a></span>'
    user_url = '<span class="text-sm leading-5 text-gray-400 group-hover:text-gray-300 transition ease-in-out duration-150"><a href="https://twitter.com/%s" target="_blank">@%s</a></span>'
    text = tweet.full_text
    if text is None:
        text = tweet.text

    if text is not None:
        for hash in tweet.hashtags:
            text = text.replace('#%s' % hash.text, hashtag_url % (quote(hash.text.encode("utf-8")), hash.text))
        for mention in tweet.user_mentions:
            text = text.replace('@%s' % mention.screen_name, user_url % (quote(mention.screen_name), mention.screen_name))
    
    x = text.rfind(' ')
    if(x != -1 and text[x+1:x+1+8] == "https://"):
        text = text[:x]

    if (hasattr(tweet, 'media') and tweet.media is not None):
        for media in tweet.media:
            if(media.type == "photo"):
                text += image_html.format(url=media.media_url_https)
            elif(media.type == "video"):
                first = next(filter(lambda variant: variant['content_type'] =='video/mp4', media.video_info['variants']), None)
                if(first is not None):
                    video_url = first['url']
                    image_url = media.media_url_https
                    text += video_html.format(image_url=image_url, url=video_url)
    if(text.startswith("RT ")):
        return text[2:]
    return text

@register.filter()
def expand_tweet_urls(tweet):
    """ Replace shortened URLs with long URLs in the twitter status
        Should be used before urlize_tweet
    """
    text = tweet.full_text
    if text is None:
        text = tweet.text
    
    urls = tweet.urls
    if(tweet.retweeted_status != None):
        text = tweet.retweeted_status.full_text
        if text is None:
            text = tweet.text
        urls = tweet.retweeted_status.urls
    if text is not None:
        for url in urls:
            text = text.replace(url.url, '<span class="text-blue-400"><a href="%s" target="_blank">%s</a></span>' % (url.expanded_url, url.url))
            
    tweet.text = text
    return tweet


@register.filter()
def twitter_text(tweet):
    text = tweet.full_text
    if text is None:
        text = tweet.text
    return text