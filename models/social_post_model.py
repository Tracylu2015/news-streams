from mongoengine import *


class UserInfo(EmbeddedDocument):
    followers_count = IntField()
    friends_count = IntField()
    id = IntField()
    location = StringField()
    profile_image_url = StringField()
    screen_name = StringField()
    verified = BooleanField()


class SocialPost(Document):
    id = ObjectIdField()
    user_info = EmbeddedDocumentField(UserInfo, fields='user_info')
    user_mentions = ListField(IntField())
    created_at = DateTimeField()
    post_id = IntField()
    text = StringField()
    hashtags = ListField(StringField())
    original_url = StringField()
    retweet_count = IntField()
    retweeted_id = StringField()
    favorite_count = IntField()
    reply_count = IntField()
    media_url = StringField()
    source = StringField()
    meta = {'collection': 'social_post'}

    def __init__(self, source, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.source = source  # twitter  or reddit
