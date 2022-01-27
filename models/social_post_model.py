from mongoengine import *


class UserInfo(EmbeddedDocument):
    followers_count = IntField()
    friends_count = IntField()
    id = IntField()
    location = StringField()
    profile_image_url = StringField()
    screen_name = StringField()
    user_mentions = ListField(IntField())
    verified = BooleanField()


class SocialPost(Document):
    id = ObjectIdField()
    user_info = EmbeddedDocumentField(UserInfo)
    created_at = DateTimeField()
    post_id = IntField()
    text = StringField()
    hashtag = ListField(StringField())
    original_url = StringField()
    retweet_count = IntField()
    retweeted_id = StringField()
    favorite_count = IntField()
    reply_count = IntField()
    media_url = StringField()
    source = StringField()

    def __init__(self, source, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.created_at = kwargs.get('created_at')
        self.post_id = kwargs.get('id')
        self.text = kwargs.get('text')
        self.user_info = UserInfo(**kwargs.get('user_info'))
        self.hashtag = kwargs.get('hashtag')
        self.original_url = kwargs.get('original_url')
        self.retweet_count = kwargs.get('retweet_count')
        self.retweeted_id = str(kwargs.get('retweeted_id', ''))
        self.favorite_count = kwargs.get('favorite_count')
        self.reply_count = kwargs.get('reply_count')
        self.media_url = kwargs.get('media_url')
        self.source = source  # twitter  or reddit
