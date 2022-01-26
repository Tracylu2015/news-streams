import os

from mongoengine import connect

mongo_host = os.getenv("MONGODB_URI")
connect(host=mongo_host)
