import collections
from genericpath import exists
import json
import logging
import os
import socket

from django.http.response import JsonResponse
from pymemcache.client.hash import HashClient
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
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
    [{"host": os.getenv("ELASTIC_HOST")}]
)


def tags(request, tag):
    # para is a url parameter passed from frontend
    s = Search(using=es, index="tstream-post-*")
    # TODO: only project post_id
    s = s.query("simple_query_string", query=tag, fields=['title', 'text']).filter('bool', must=[Q('exists', field="medial_url")]).sort(
        {
            "user_info.friends_count": {
                "order": "desc"
            }
        },
        {
            "user_info.followers_count": "desc"
        },
        "_score")[:100]
    response = s.execute()
    # a list of post_id return from elastic search
    data = []
    seen = set()
    for hit in response:
        if hit.post_id not in seen:
            seen.add(hit.post_id)
            data.append(hit.post_id)
    print(data)
    posts = SocialPost.objects(post_id__in=data)

    result = []
    for p in posts:
        p = json.loads((p.to_json()))
        result.append(p)
    return JsonResponse(result, safe=False)
