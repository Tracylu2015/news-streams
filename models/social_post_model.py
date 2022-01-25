class SocialPost:
    def __init__(self, type, **kwargs):
        self.created_at = kwargs.get('created_at')
        self.id = kwargs.get('id')
        self.text = kwargs.get('text')
        self.user_info = kwargs.get('user_info')
        self.hashtag = kwargs.get('hashtag')
        self.original_url = kwargs.get('original_url')
        self.retweet_count = kwargs.get('retweet_count')
        self.retweeted_id = str(kwargs.get('retweeted_id', ''))
        self.favorite_count = kwargs.get('favorite_count')
        self.reply_count = kwargs.get('reply_count')
        self.media_url = kwargs.get('media_url')
        self.type = type  # twitter  or reddit
