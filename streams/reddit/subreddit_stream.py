import requests


class SubredditStream:
    '''
    wallstreetbets
    stocks
    investing
    CryptoCurrency
    bitcoin
    CryptoMarkets
    btc
    '''

    URL = 'https://www.reddit.com/r/{subreddit}.json?limit=30'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    def __init__(self, subreddit, last_scrape_time=None) -> None:
        super().__init__()
        self.subreddit = subreddit
        self.last_scrape_time = last_scrape_time

    def fetch(self):
        resp = requests.get(self.URL.format(subreddit=self.subreddit), headers=self.headers)
        return resp.json()
