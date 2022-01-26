import json

from models.parse_json_to_model import parse_twitter_stream
from streams.kafka_consumer import KafkaConsumer


def start_consumer():
    consumer = KafkaConsumer()
    topics = ["twitter_stream"]
    for msg in consumer.basic_consume_loop(topics):
        # read from kafka server and insert into MongoDB
        parse_twitter_stream(json.loads(msg)).save()

    consumer.shutdown()


if __name__ == '__main__':
    start_consumer()
