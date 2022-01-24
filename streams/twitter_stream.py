from streams.kafka_client import KafkaClient
from streams.twitter.filtered_stream import TwitterFilteredStream


def start_twitter():
    producer = KafkaClient()
    test = TwitterFilteredStream(producer)
    test.filter(languages=['en'], track=['#stock', '#nasdq', '#nyse',
                                         '#stocks', '#stockmarket', '#stockstowatch',
                                         '#crypto', '#bitcoin', '#cryptocurrency'])
    producer.on_stream_terminate()


if __name__ == '__main__':
    start_twitter()
