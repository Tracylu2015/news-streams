from mongoengine import *


class UserInfo(DynamicEmbeddedDocument):
    followers_count = IntField()
    friends_count = IntField()
    id = StringField()
    location = StringField()
    profile_image_url = StringField()
    screen_name = StringField()
    verified = BooleanField()


class SocialPost(DynamicDocument):
    id = ObjectIdField()
    user_info = EmbeddedDocumentField(UserInfo, fields='user_info')
    user_mentions = ListField(StringField())
    created_at = DateTimeField()
    post_id = StringField()
    text = StringField()
    title = StringField()
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
