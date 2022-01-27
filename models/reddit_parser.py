import datetime

import time
from dateutil.tz import tzutc

from models.social_post_model import SocialPost


def parse_reddit_post(data):
    '''
    :param data: json response from reddit
    :return: SocialPost obj
    '''
    data = data.get('data', {})
    user_info = {
        'screen_name': data.get('author', '')
    }
    media_url = None
    for image in data.get('preview', {}).get('images', []):
        resolutions = image.get('resolutions', [])
        if resolutions:
            media_url = resolutions[-1].get('url')
            break
    result = {
        'created_at': datetime.datetime.fromtimestamp(data.get('created_utc', time.time()), tz=tzutc()),
        'post_id': data.get('id', ''),
        'text': data.get('selftext', ''),
        'title': data.get('title', ''),
        'hashtags': [],
        'original_url': data.get('url'),
        'retweet_count': data.get('num_crossposts', 0),
        'favorite_count': data.get('ups', 0),
        'reply_count': data.get('num_comments', 0),
        'user_info': user_info,
        'media_url': media_url
    }
    return SocialPost(source='reddit', **result)
