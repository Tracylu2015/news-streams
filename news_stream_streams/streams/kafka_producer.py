import json
import os

from confluent_kafka import Producer
from streams.stream_data import StreamData


class KafkaProducer(StreamData):
    def __init__(self):
        # get kafka host from environment variable
        servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
        self.producer = Producer(
            {
                'bootstrap.servers': servers,
                'compression.type': 'snappy'  # compress text to send to server
            }
        )

    # set producer msg to kafka
    def on_stream_data(self, topic_name, json_data):
        json_string = json.dumps(json_data)
        self.producer.produce(topic_name, json_string.encode('utf-8'))

    def on_stream_terminate(self):
        self.producer.flush()
