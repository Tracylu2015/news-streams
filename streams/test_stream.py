from pprint import pprint

from streams.kafka_client import KafkaClient
from streams.reddit.subreddit_stream import SubredditStream
from streams.twitter.filtered_stream import TwitterFilteredStream


def test_twitter():
    producer = KafkaClient()
    test = TwitterFilteredStream(producer)
    test.filter(languages=['en'], track=['#stock', '#nasdq', '#nyse', '#stocks', '#stockmarket', '#stockstowatch',
                                         '#crypto', '#bitcoin', '#cryptocurrency'])
    producer.on_stream_terminate()

test_twitter()

# def test_reddit():
#     # test = SubredditStream('stocks')
#     test = SubredditStream('CryptoCurrency')
#     pprint(test.fetch())
#
#
# test_reddit()
