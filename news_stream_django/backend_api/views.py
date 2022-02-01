import collections
import json
import logging
import os
import socket

from django.http.response import JsonResponse
from django.core.cache import caches
from pymemcache.client.hash import HashClient
from django.shortcuts import render

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
