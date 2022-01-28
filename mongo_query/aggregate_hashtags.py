from django.utils import timezone
from django.utils.datetime_safe import datetime

[
    {
        '$match': {
            'created_at': {
                '$gte': datetime(2022, 1, 27, 23, 5, 5, tzinfo=timezone.utc)
            }
        }
    }, {
    '$unwind': {
        'path': '$hashtags'
    }
}, {
    '$project': {
        'id': 1,
        'text': 1,
        'hashtags': 1
    }
}, {
    '$group': {
        '_id': '$hashtags',
        'hashtags_count': {
            '$sum': 1
        }
    }
}, {
    '$sort': {
        'hashtags_count': -1
    }
}, {
    '$limit': 30
}
]