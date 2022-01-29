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
    data = [
        {"name": "BITCOIN", "count": 12230},
        {"name": "CRYPTO", "count": 12184},
        {"name": "CRYPTOCURRENCY", "count": 3683},
        {"name": "NFT", "count": 3425},
        {"name": "BTC", "count": 839},
        {"name": "ETH", "count": 688},
        {"name": "NFTCOMMUNITY", "count": 654},
        {"name": "AIRDROP", "count": 623},
        {"name": "BSCGEM", "count": 598},
        {"name": "NFTGIVEAWAY", "count": 543},
        {"name": "NFTS", "count": 517},
        {"name": "GAMING", "count": 503},
        {"name": "SHIBFENINU", "count": 474},
        {"name": "DEFI", "count": 408},
        {"name": "SUSTAINABLE", "count": 406},
        {"name": "GRN", "count": 405},
        {"name": "BINANCE", "count": 338},
        {"name": "METAVERSE", "count": 331},
        {"name": "BSC", "count": 321},
        {"name": "NFTCOLLECTOR", "count": 317},
        {"name": "CRYPTOGIVEAWAY", "count": 307},
        {"name": "SHIBA", "count": 307},
        {"name": "BLOCKCHAIN", "count": 306},
        {"name": "NFTGIVEAWAYS", "count": 298},
        {"name": "DOGECOIN", "count": 256}
    ]

    return JsonResponse(data, safe=False)
