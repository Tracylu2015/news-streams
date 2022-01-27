import unittest
import json
from datetime import datetime
from dateutil.tz import tzutc

from models.parse_json_to_model import parse_twitter_stream
from models.reddit_parser import parse_reddit_post
from models.social_post_model import UserInfo


class TestParseModel(unittest.TestCase):

    def test_parse_model(self):
        with open('json/twitter_media.json') as file:
            self.json_obj = json.load(file)
        data = parse_twitter_stream(self.json_obj)
        self.assertEqual(data.post_id, '1485817898056953857')
        self.assertIsInstance(data.user_info, UserInfo)
        self.assertEqual(data.user_mentions, [1348300561104265217, 1454415315673227267])
        self.assertEqual(data.created_at, datetime(2022, 1, 25, 3, 32, 46, tzinfo=tzutc()))
        self.assertEqual(data.text,
                         'RT @Jay90566398: #Facts  JOIN BEFORE WE TAKE OFF 🥷🥷🔥🔥STILL SUPER EARLY‼️‼️ @Shib_nobi #SHINJA #SHINJAISTHENEXT1000X #Shibnobi')
        self.assertEqual(data.original_url, 'https://twitter.com/i/web/status/1485778455882993664')
        self.assertEqual(data.retweet_count, 1)
        self.assertEqual(data.favorite_count, 5)
        self.assertEqual(data.reply_count, 3)
        self.assertEqual(data.retweeted_id, None)
        self.assertEqual(data.source, 'twitter')
        self.assertEqual(len(data.hashtags), 4)
        self.assertEqual(data.hashtags, ['Facts', 'SHINJA', 'SHINJAISTHENEXT1000X', 'Shibnobi'])
        self.assertEqual(data.media_url, 'https://pbs.twimg.com/media/FJz4iDQakAE_-Xw.jpg')
        self.assertEqual(data.user_mentions, [1348300561104265217, 1454415315673227267])

    def test_parse_reddit_post(self):
        with open('json/reddit_post.json') as file:
            json_obj = json.load(file)
        data = parse_reddit_post(json_obj)
        self.assertNotEqual(data, None)
        self.assertIsInstance(data.user_info, UserInfo)
        self.assertEqual(data.user_mentions, [])
        self.assertEqual(data.created_at, datetime(2022, 1, 26, 19, 15, 52, tzinfo=tzutc()))
        self.assertEqual(data.post_id, 'sddv41')
        self.assertEqual(len(data.text), 1011)
        self.assertEqual(len(data.title), 272)
        self.assertEqual(data.original_url,
                         'https://www.reddit.com/r/CryptoCurrency/comments/sddv41/the_fed_decision_was_extremely_encouraging_and/')
        self.assertEqual(data.retweet_count, 0)
        self.assertEqual(data.favorite_count, 341)
        self.assertEqual(data.reply_count, 266)
        self.assertEqual(data.retweeted_id, None)
        self.assertEqual(data.source, 'reddit')
        self.assertEqual(len(data.hashtags), 0)
        self.assertEqual(data.media_url,
                         'https://external-preview.redd.it/s786qgzk68tIp_H9M3qcZEtbH0Svuqak9SBuoYyKgm4.png?width=1080&amp;crop=smart&amp;format=pjpg&amp;auto=webp&amp;s=21a568a972c79a8795594d81710b59fc4d595aa9')
        self.assertEqual(data.user_mentions, [])


if __name__ == '__main__':
    unittest.main()
