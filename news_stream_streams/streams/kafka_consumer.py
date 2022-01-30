import os

from confluent_kafka import Consumer
from prometheus_client import Counter


class KafkaConsumer:

    def __init__(self):
        servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
        group = os.getenv('KAFKA_GROUP_CONSUMER')
        auto_commit = os.getenv('KAFKA_AUTO_COMMIT', 'True') == 'True'
        conf = {'bootstrap.servers': servers,
                'group.id': group,
                'enable.auto.commit': auto_commit,
                'auto.offset.reset': 'smallest'}

        self.consumer = Consumer(conf)
        self.running = True
        self.counter = Counter('twitter_streams_consumer_processed', 'Total consumed tweets')

    # basic poll loop
    def basic_consume_loop(self, topics):
        try:
            self.consumer.subscribe(topics)

            while self.running:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    print(msg.error())
                    continue
                else:
                    # yield  is used like return, function will return a generator
                    self.counter.inc()
                    yield msg
        finally:
            # Close down consumer to commit final offsets.
            self.consumer.close()

    def shutdown(self):
        self.running = False
