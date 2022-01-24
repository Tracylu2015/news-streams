import os

from streams.kafka_client import KafkaClient
from streams.reddit.subreddit_stream import SubredditStream
from prometheus_client import start_http_server


def start_reddit():
    producer = KafkaClient()
    stream = SubredditStream(os.getenv('SUBREDDIT', 'CryptoCurrency'), producer)
    stream.fetch()
    producer.on_stream_terminate()


if __name__ == '__main__':
    start_http_server(8080)
    start_reddit()
