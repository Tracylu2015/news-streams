import json
from collections import defaultdict
from pprint import pprint
from dateutil import parser

from models.social_post_model import SocialPost

TOP_LEVEL_KEYS = {'created_at', 'id', 'text', 'user', 'entities', 'reply_count', 'retweet_count', 'favorite_count',
                  'retweeted_status'}
USER_LEVEL_KEYS = {'id', 'screen_name', 'location', 'verified', 'followers_count', 'friends_count', 'profile_image_url'}
ENTITIES_LEVEL_KEYS = {'hashtags', 'user_mentions'}


def parse_json(jsonObj):
    # print(jsonfile.keys())
    data = {}
    user_info = {}
    hashtag = defaultdict(list)
    for key in jsonObj.keys():
        if key in TOP_LEVEL_KEYS:
            data[key] = jsonObj[key]
    for k, v in data["user"].items():
        if k in USER_LEVEL_KEYS:
            user_info[k] = v

    for k, v in data["entities"].items():
        if k in ENTITIES_LEVEL_KEYS:
            data[k] = v

    user_info["user_mentions"] = []
    for ele in data["user_mentions"]:
        user_info["user_mentions"].append(ele["id"])

    for ele in data["hashtags"]:
        hashtag["hashtags"].append(ele["text"])

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

    data["user_info"] = user_info
    data["hashtag"] = hashtag["hashtags"]
    data["created_at"] = parser.parse(data["created_at"])
    del data["user"]
    del data["entities"]
    del data["hashtags"]
    del data["retweeted_status"]
    del data["user_mentions"]

    twitter_post = SocialPost(source="twitter", **data)

    return twitter_post


if __name__ == '__main__':
    with open("../json/twitter_media.json") as f:
        jsonfile = json.load(f)
        pprint(parse_json(jsonfile).__dict__)
