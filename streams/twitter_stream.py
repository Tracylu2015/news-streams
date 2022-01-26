from streams.kafka_producer import KafkaProducer
from streams.twitter.filtered_stream import TwitterFilteredStream
from prometheus_client import start_http_server


def start_twitter():
    producer = KafkaProducer()
    test = TwitterFilteredStream(producer)
    test.filter(languages=['en'], track=['#stock', '#nasdq', '#nyse',
                                         '#stocks', '#stockmarket', '#stockstowatch',
                                         '#crypto', '#bitcoin', '#cryptocurrency'])
    producer.on_stream_terminate()


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    start_twitter()
