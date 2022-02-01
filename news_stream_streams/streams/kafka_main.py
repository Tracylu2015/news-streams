import json
import logging
import os

from models.parse_json_to_model import parse_twitter_stream
from prometheus_client import start_http_server
from streams.kafka_consumer import KafkaConsumer
from elasticsearch import Elasticsearch
from datetime import datetime

es = Elasticsearch(
    [{"host": os.getenv('ELASTIC_HOST')}]
)


def start_consumer():
    logging.basicConfig(level=logging.WARN)
    consumer = KafkaConsumer()
    topics = ["twitter_stream"]
    for msg in consumer.basic_consume_loop(topics):
        # read from kafka server and insert into MongoDB
        post = parse_twitter_stream(json.loads(msg.value().decode('utf-8')))
        post.save()
        es_doc = json.loads(post.to_json())
        if '_id' in es_doc:
            del es_doc['_id']
        es.index(
            index="tstream-post-{suffix}".format(suffix=datetime.today().strftime('%Y.%m.%d')),
            document=es_doc,
            id=es_doc.get('post_id')
        )

    consumer.shutdown()


if __name__ == '__main__':
    start_http_server(8000)
    start_consumer()
