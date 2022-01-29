import json

from models.parse_json_to_model import parse_twitter_stream
from prometheus_client import start_http_server
from streams.kafka_consumer import KafkaConsumer


def start_consumer():
    consumer = KafkaConsumer()
    topics = ["twitter_stream"]
    data = {}
    for msg in consumer.basic_consume_loop(topics):
        # read from kafka server and insert into MongoDB
        parse_twitter_stream(json.loads(msg.value().decode('utf-8'))).save()

    consumer.shutdown()


if __name__ == '__main__':
    start_http_server(8000)
    start_consumer()
