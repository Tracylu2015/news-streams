import collections
import json

from django.http.response import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from backend_api.models import SocialPost


def index(request):
    posts = SocialPost.objects.limit(5)
    data = []
    for p in posts:
        p = json.loads((p.to_json()))
        data.append(p)
    return JsonResponse(data, safe=False)
    # return HttpResponse("Hello, world. You're at the polls index.")


def trending(request):
    data = {
        "BITCOIN": 12230,
        "CRYPTO": 12184,
        "CRYPTOCURRENCY": 3683,
        "NFT": 3425,
        "BTC": 839,
        "ETH": 688,
        "NFTCOMMUNITY": 654,
        "AIRDROP": 623,
        "BSCGEM": 598,
        "NFTGIVEAWAY": 543,
        "NFTS": 517,
        "GAMING": 503,
        "SHIBFENINU": 474,
        "DEFI": 408,
        "SUSTAINABLE": 406,
        "GRN": 405,
        "BINANCE": 338,
        "METAVERSE": 331,
        "BSC": 321,
        "NFTCOLLECTOR": 317,
        "CRYPTOGIVEAWAY": 307,
        "SHIBA": 307,
        "BLOCKCHAIN": 306,
        "NFTGIVEAWAYS": 298,
        "DOGECOIN": 256
    }
    # counter = collections.Counter()
    # for k, v in data.items():
    #     k = k.upper()
    #     counter[k] += counter.get(k, 0) + v
    return JsonResponse(data)