from django_mongoengine import DynamicDocument, DynamicEmbeddedDocument, fields


class UserInfo(DynamicEmbeddedDocument):
    followers_count = fields.IntField()
    friends_count = fields.IntField()
    id = fields.StringField()
    location = fields.StringField()
    profile_image_url = fields.StringField()
    screen_name = fields.StringField()
    verified = fields.BooleanField()


class SocialPost(DynamicDocument):
    id = fields.ObjectIdField()
    user_info = fields.EmbeddedDocumentField(UserInfo, fields='user_info')
    user_mentions = fields.ListField(fields.StringField())
    created_at = fields.DateTimeField()
    post_id = fields.StringField()
    text = fields.StringField()
    title = fields.StringField()
    hashtags = fields.ListField(fields.StringField())
    original_url = fields.StringField()
    retweet_count = fields.IntField()
    retweeted_id = fields.StringField()
    favorite_count = fields.IntField()
    reply_count = fields.IntField()
    media_url = fields.StringField()
    source = fields.StringField()
    meta = {'collection': 'social_post'}

    def __init__(self, source, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.source = source  # twitter  or reddit