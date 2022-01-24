import os
import tweepy
from prometheus_client import Counter


class TwitterFilteredStream(tweepy.Stream):

    def __init__(self, producer):
        super().__init__(
            os.environ.get("CONSUMER_KEY"),
            os.environ.get("CONSUMER_SECRET"),
            os.environ.get("ACCESS_TOKEN"),
            os.environ.get("ACCESS_TOKEN_SECRET")
        )
        self.producer = producer
        # prometheus Counter
        self.counter = Counter('twitter_streams_document_received', 'Total number of streams')

    def on_status(self, status):
        # call counter function to increment counts
        self.counter.inc()
        json_attr = getattr(status, '_json')
        self.producer.on_stream_data("twitter_stream", json_attr)
