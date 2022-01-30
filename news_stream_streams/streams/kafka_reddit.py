import json
from pprint import pprint

from models.reddit_parser import parse_reddit_post
from prometheus_client import start_http_server
from kafka_consumer import KafkaConsumer


def start_consumer():
    consumer = KafkaConsumer()
    topics = ["reddit_stream"]
    data = {}
    for msg in consumer.basic_consume_loop(topics):
        # read from kafka server and insert into MongoDB
        parse_reddit_post(json.loads(msg.value().decode('utf-8'))).save()

    consumer.shutdown()


if __name__ == '__main__':
    start_http_server(8000)
    start_consumer()
