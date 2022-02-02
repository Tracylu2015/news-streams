import collections
import json
import logging
import os
import socket

from django.http.response import JsonResponse
from pymemcache.client.hash import HashClient
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import os

# Create your views here.
from django.http import HttpResponse

from backend_api.models import SocialPost

cache_address = socket.gethostbyname_ex(os.getenv('MEMCACHED_SERVICE'))[-1]
cache_client = HashClient(
    servers=cache_address,
    allow_unicode_keys=True,
    no_delay=True,
    ignore_exc=True,
    use_pooling=True,
    max_pool_size=4
)


def index(request):
    posts = SocialPost.objects.limit(5)
    data = []
    for p in posts:
        p = json.loads((p.to_json()))
        data.append(p)
    return JsonResponse(data, safe=False)
    # return HttpResponse("Hello, world. You're at the polls index.")


def trending(request):
    data = cache_client.get('top_appeared_tags')
    if data:
        return JsonResponse(json.loads(data), safe=False)
    return JsonResponse({}, safe=False)


es = Elasticsearch(
    [{"host": os.getenv("ELASTICHOST")}]
)


def tags(request, para):
    # para is a url parameter passed from frontend
    s = Search(using=es, index="tstream-post-*")
    # TODO: only project post_id
    s = s.query("simple_query_string", query=para, fields=['title', 'text'])
    response = s.execute()
    # a list of post_id return from elastic search
    data = []
    for hit in response:
        data.append(hit.post_id)
    posts = SocialPost.find({"post_id": {"$in": data}}).objects
    result = []
    for p in posts:
        p = json.loads((p.to_json()))
        result.append(p)
    return JsonResponse(result, safe=False)
