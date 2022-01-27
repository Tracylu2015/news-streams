import json
from pprint import pprint
from dateutil import parser

from models.social_post_model import SocialPost

TOP_LEVEL_KEYS = {'created_at', 'id', 'text', 'user', 'entities', 'reply_count', 'retweet_count', 'favorite_count',
                  'retweeted_status'}
USER_LEVEL_KEYS = {'id', 'screen_name', 'location', 'verified', 'followers_count', 'friends_count', 'profile_image_url'}
ENTITIES_LEVEL_KEYS = {'hashtags', 'user_mentions'}
CLEANUP_KEYS = ['id', 'user', 'entities', 'retweeted_status']

def parse_twitter_stream(jsonObj):
    # print(jsonfile.keys())
    data = {}
    user_info = {}
    hashtags = []
    for key in jsonObj.keys():
        if key in TOP_LEVEL_KEYS:
            data[key] = jsonObj[key]
    for k, v in data["user"].items():
        if k in USER_LEVEL_KEYS:
            user_info[k] = v

    for k, v in data["entities"].items():
        if k in ENTITIES_LEVEL_KEYS:
            data[k] = v

    user_mentions = []
    for ele in data["user_mentions"]:
        user_mentions.append(str(ele["id"]))

    for ele in data["hashtags"]:
        hashtags.append(ele["text"])

    tid = data.get("retweeted_status", {}).get("id")
    if tid:
        url = "https://twitter.com/i/web/status/{id}".format(id=tid)
        data["original_url"] = url
    else:
        data["original_url"] = ""

    medias = data.get("retweeted_status", {}).get("quoted_status", {}).get("entities", {}).get("media", [])
    for m in medias:
        media_url = m.get("media_url_https", "")
        if not media_url:
            data["media_url"] = ""
        if media_url:
            data["media_url"] = media_url
            break

    user_info['id'] = str(user_info['id'])
    data["user_info"] = user_info
    data["hashtags"] = hashtags
    data["user_mentions"] = user_mentions
    data["post_id"] = str(data["id"])
    data["created_at"] = parser.parse(data["created_at"])
    for key in CLEANUP_KEYS:
        if key in data:
            del data[key]

    twitter_post = SocialPost(source="twitter", **data)

    return twitter_post


if __name__ == '__main__':
    with open("../json/twitter_media.json") as f:
        jsonfile = json.load(f)
        pprint(parse_twitter_stream(jsonfile).__dict__)
