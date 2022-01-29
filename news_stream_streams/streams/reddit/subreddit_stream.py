import logging
import os
import socket

import requests
import time
from prometheus_client import Counter
from pymemcache.client.hash import HashClient


class SubredditStream:
    DEFAULT_SUBREDDIT = [
        'wallstreetbets',
        'stocks',
        'investing',
        'CryptoCurrency',
        'bitcoin',
        'CryptoMarkets',
        'btc'
    ]

    URL = 'https://www.reddit.com/r/{subreddit}/new.json?limit={page_size}'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/39.0.2171.95 Safari/537.36'}

    def __init__(self, subreddit, on_stream_listener) -> None:
        super().__init__()
        if subreddit is not None:
            self.subreddit = subreddit
        else:
            self.subreddit = self.DEFAULT_SUBREDDIT
        self.on_stream_listener = on_stream_listener
        self.running = True
        self.reddit_pooling_sleep = int(os.getenv('REDDIT_POOLING_SLEEP', '60'))
        self.reddit_dedup_ttl = int(os.getenv('REDDIT_DEDUP_TTL', '86400'))
        self.reddit_page_size = int(os.getenv('REDDIT_PAGE_SIZE', '30'))
        try:
            # memcached-headless.news-stream.svc.cluster.local
            cache_address = socket.gethostbyname_ex(os.getenv('MEMCACHED_SERVICE'))[-1]
        except socket.gaierror:
            cache_address = []
        if cache_address:
            logging.info("Caching is enabled: %s" % cache_address)
            self.cache_client = HashClient(cache_address)
        else:
            self.cache_client = None

        # prometheus Counter and add label names for the 3rd param
        self.counter = Counter('reddit_streams_document_received', 'Total number of streams', ['source'])
        self.dedup_counter = Counter('reddit_streams_document_deduplcated', 'Total number of streams deduplcated',
                                ['source'])

    def fetch(self):
        if self.on_stream_listener is None:
            return
        while self.running:
            for subreddit in self.subreddit:
                logging.info("Fetching subreddit: %s" % subreddit)
                resp = requests.get(
                    self.URL.format(
                        subreddit=subreddit,
                        page_size=self.reddit_page_size
                    ),
                    headers=self.HEADERS
                )
                if resp.status_code == 429:
                    logging.info("Received 429 response")
                    time.sleep(self.reddit_pooling_sleep)
                    continue
                if resp.status_code >= 400:
                    logging.info("Received error response")
                    time.sleep(self.reddit_pooling_sleep)
                    continue
                for elem in resp.json().get('data', {}).get('children', []):
                    # call counter to increment counts
                    data = elem.get('data', {})
                    post_id = data.get('id')
                    if not post_id or self.is_dup(post_id, subreddit):
                        continue
                    self.counter.labels(subreddit).inc()
                    self.on_stream_listener.on_stream_data('reddit_stream', data)
                time.sleep(self.reddit_pooling_sleep)

    def is_dup(self, post_id, subreddit):
        if not self.cache_client:
            return False
        result = self.cache_client.get(post_id)
        if result:
            self.dedup_counter.labels(subreddit).inc()
            return True
        self.cache_client.set(post_id, exptime=time.time()+self.reddit_dedup_ttl)
        return False
