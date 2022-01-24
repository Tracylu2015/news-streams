import requests
import time


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

    URL = 'https://www.reddit.com/r/{subreddit}.json?limit=10'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/39.0.2171.95 Safari/537.36'}

    def __init__(self, on_stream_listener, subreddit) -> None:
        super().__init__()
        if subreddit is not None:
            self.subreddit = subreddit
        else:
            self.subreddit = self.DEFAULT_SUBREDDIT
        self.on_stream_listener = on_stream_listener
        self.running = True

    def fetch(self):
        if self.on_stream_listener is None:
            return
        while self.running:
            for subreddit in self.subreddit:
                resp = requests.get(self.URL.format(subreddit=subreddit), headers=self.HEADERS)
                if resp.status_code == 429:
                    time.sleep(60)
                    continue
                if resp.status_code >= 400:
                    time.sleep(30)
                    continue
                for data in resp.json().get('data', {}).get('children', []):
                    self.on_stream_listener.on_stream_data(data)
                time.sleep(30)
