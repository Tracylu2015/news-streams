import json
import os
import socket
from datetime import datetime
from datetime import timedelta

import pymongo
from pymemcache.client.hash import HashClient

pipeline = [
    {
        '$match': {
            'created_at': {
                '$gte': datetime.now() - timedelta(hours=1)
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

bitcoin = {"BITCOIN", "BTC"}
crypto = {"CRYPTO", "CRYPTOCURRENCY"}
nft = {"NFT", "NFTGIVEAWAY", "NFTART", "NFTS", "NFTCOMMUNITY", "NFTCOLLECTOR"}


def update_trending_tags():
    my_client = pymongo.MongoClient(os.getenv("MONGODB_URI"))
    mydb = my_client["news-streams"]
    mycol = mydb["social_post"]
    my_doc = mycol.aggregate(pipeline)

    result = []
    for d in my_doc:
        data = {"name": d["_id"], "count": d["hashtags_count"]}
        result.append(data)

    btc = {"tags": [], "count": 0}
    cry = {"tags": [], "count": 0}
    nfts = {"tags": [], "count": 0}
    data = []
    for elem in result:
        if elem["name"] in bitcoin:
            btc["tags"].append(elem["name"])
            btc["count"] += elem["count"]
            btc["name"] = "BITCOIN"

        elif elem["name"] in crypto:
            cry["tags"].append(elem["name"])
            cry["count"] += elem["count"]
            cry["name"] = "CRYPTO"

        elif elem["name"] in nft:
            nfts["tags"].append(elem["name"])
            nfts["count"] += elem["count"]
            nfts["name"] = "NFT"

        else:
            data.append(elem)

    data.append(btc)
    data.append(nfts)
    data.append(cry)
    data = sorted(data, key=lambda x: x["count"], reverse=True)

    # resolve DNS
    cache_address = socket.gethostbyname_ex(os.getenv('MEMCACHED_SERVICE'))[-1]
    # pymemcache to choose which server to set/get the values from.
    # It will also automatically rebalance depending on if a server goes down.
    cache_client = HashClient(
        servers=cache_address,
        allow_unicode_keys=True,
        no_delay=True,
        ignore_exc=True
    )
    # save into cache
    cache_client.set("top_appeared_tags", data)


if __name__ == '__main__':
    update_trending_tags()
