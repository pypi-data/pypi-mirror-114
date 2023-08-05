import pymongo
import requests
import datetime
import urllib.parse
from requests.models import Response
from typing import Any, Dict, Union
from pymongo import MongoClient
from pymongo.collection import Collection


class CachedRequestClient:
    __mongoClient: MongoClient
    __headers: Dict

    def __init__(self, mongo_client: MongoClient, headers=None):
        if headers is None:
            headers = dict()
        self.__mongoClient = mongo_client
        self.__headers = headers

    def get(self, url, mode='nested', params=None, no_cache=False, time_diff_allowance=datetime.timedelta(days=1)):

        if no_cache:
            self.__get_from_http__(url, params)
            return

        parsed_url = urllib.parse.urlsplit(url)

        db = self.__mongoClient.get_database(parsed_url.hostname.replace('.', '-'))
        collection = db.get_collection(parsed_url.path) if mode == 'nested' else db.get_collection('requests')

        mongo_filter = params if mode == 'nested' else {'url': parsed_url.path}

        now: datetime = datetime.datetime.utcnow()
        most_recent_match: Union[Dict, None] = collection.find_one(
            mongo_filter, sort=[('time', pymongo.DESCENDING)]
        )

        if most_recent_match is not None:
            time_since_most_recent_request = now - most_recent_match['time']

            if time_since_most_recent_request > time_diff_allowance:
                return self.__get_from_http__(collection, url, params, mongo_filter)
            else:
                return most_recent_match['response']

        else:
            return self.__get_from_http__(collection, url, params, mongo_filter)

    def __get_collection_from_url__(self, url) -> Collection:
        parsed_url = urllib.parse.urlsplit(url)
        return self.__mongoClient.get_database(parsed_url.hostname.replace('.', '-')).get_collection(parsed_url.path)

    def __get_from_http__(self, collection, url, params=None, mongo_filter=None, **kwargs):
        r: Response = requests.get(url, params, **kwargs, headers=self.__headers)
        doc = {**mongo_filter, 'time': datetime.datetime.utcnow(), 'response': r.json()}
        collection.insert_one(doc)
        return r.json()
