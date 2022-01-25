import unittest
import json

from models.parse_json_to_model import parse_json
from models.social_post_model import UserInfo


class TestParseModel(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        with open("json/twitter_media.json") as file:
            self.json_obj = json.load(file)

    def test_parse_model(self):
        data = parse_json(self.json_obj)
        self.assertEqual(data.id, 1485817898056953857)
        self.assertEqual(len(data.hashtag), 4)
        self.assertIsInstance(data.user_info, UserInfo)
        self.assertEqual(data.media_url, "https://pbs.twimg.com/media/FJz4iDQakAE_-Xw.jpg")


if __name__ == '__main__':
    unittest.main()
