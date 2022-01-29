import logging
import os

from kafka_producer import KafkaProducer
from reddit.subreddit_stream import SubredditStream
from prometheus_client import start_http_server


def start_reddit():
    logging.basicConfig(level=logging.getLevelName(os.getenv('LOG_LEVEL', 'DEBUG').upper()))

    producer = KafkaProducer()
    stream = SubredditStream(os.getenv('SUBREDDIT'), producer)
    stream.fetch()
    producer.on_stream_terminate()


if __name__ == '__main__':
    start_http_server(8080)
    start_reddit()
