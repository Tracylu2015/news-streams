import os

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

es = Elasticsearch(
    [{"host": "192.168.31.45"}]
)


def getSearchIds():
    s = Search(using=es, index="tstream-post-*")
    s = s.query("simple_query_string", query='BTC', fields=['title', 'text'])
    response = s.execute()

    data = []
    for hit in response:
        data.append(hit.post_id)



getSearchIds()
