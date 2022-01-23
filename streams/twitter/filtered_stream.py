import os
import tweepy


class TwitterFilteredStream(tweepy.Stream):

    def __init__(self, producer):
        super().__init__(
            os.environ.get("CONSUMER_KEY"),
            os.environ.get("CONSUMER_SECRET"),
            os.environ.get("ACCESS_TOKEN"),
            os.environ.get("ACCESS_TOKEN_SECRET")
        )
        self.producer = producer

    def on_status(self, status):
        json_attr = getattr(status, '_json')
        self.producer.on_stream_data("twitter_stream", json_attr)

