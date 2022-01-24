import os

from streams.kafka_client import KafkaClient
from streams.reddit.subreddit_stream import SubredditStream


def start_reddit():
    producer = KafkaClient()
    stream = SubredditStream(os.getenv('SUBREDDIT', 'CryptoCurrency'), producer)
    stream.fetch()
    producer.on_stream_terminate()


if __name__ == '__main__':
    start_reddit()
