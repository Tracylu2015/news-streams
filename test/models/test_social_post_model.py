import unittest
import json

from models.parse_json_to_model import parse_twitter_stream
from models.social_post_model import UserInfo


class TestParseModel(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        with open("json/twitter_media.json") as file:
            self.json_obj = json.load(file)

    def test_parse_model(self):
        data = parse_twitter_stream(self.json_obj)
        self.assertEqual(data.post_id, 1485817898056953857)
        self.assertEqual(len(data.hashtags), 4)
        self.assertIsInstance(data.user_info, UserInfo)
        self.assertEqual(data.media_url, "https://pbs.twimg.com/media/FJz4iDQakAE_-Xw.jpg")
        self.assertEqual(data.user_mentions, [1348300561104265217, 1454415315673227267])


if __name__ == '__main__':
    unittest.main()
