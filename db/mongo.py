import pymongo
import os

from dotenv import load_dotenv
from enum import Enum

load_dotenv()


class CollectionName(Enum):
    CARRIER = 'CARRIER'
    DIP_SECRET_LENGTH_TEST = 'DIP_SECRET_LENGTH_TEST'
    DIP_CONST_SECRET_TEST = 'DIP_CONST_SECRET_TEST'
    DIP_RANDOM_FIXED_LENGTH_SECRET_TEST = 'DIP_RANDOM_FIXED_LENGTH_SECRET_TEST'
    PDH_CONST_SECRET_TEST = 'PDH_CONST_SECRET_TEST'
    PDH_CONST_CARRIER_TEST = 'PDH_CONST_CARRIER_TEST'


class MongoClient:
    def __init__(self) -> None:
        db_url = os.environ['MONGO_DB_URL'].format(password=os.environ['MONGO_DB_PASSWORD'])
        self._client = pymongo.MongoClient(db_url)

    def validate_insert(self, query: dict[str, any]):
        if 'collection' not in query:
            raise KeyError('Required key \'collection\' is missing in query')

        if 'data' not in query:
            raise KeyError('Required key \'data\' is missing in query')

    def validate_update(self, query: dict[str, any]):
        if 'collection' not in query:
            raise KeyError('Required key \'collection\' is missing in query')

        if 'query' not in query:
            raise KeyError('Required key \'query\' is missing in query')

        if 'update' not in query:
            raise KeyError('Required key \'new_vals\' is missing in query')

    def validate_find(self, query: dict[str, any]):
        if 'collection' not in query:
            raise KeyError('Required key \'collection\' is missing in query')

        if 'query' not in query:
            raise KeyError('Required key \'query\' is missing in query')

    def insert_one(self, query: dict[str, any]):
        self.validate_insert(query)
        col = self._client.db_stego[query['collection'].name]

        return col.insert_one(query['data'])

    def insert_many(self, query: dict[str, any]):
        self.validate_insert(query)
        col = self._client.db_stego[query['collection'].name]

        return col.insert_many(query['data'])

    def update_one(self, query: dict[str, any]):
        self.validate_update(query)
        col = self._client.db_stego[query['collection'].name]

        col.update_one(query['query'], query['update'])

    def update_many(self, query: dict[str, any]):
        self.validate_update(query)
        col = self._client.db_stego[query['collection'].name]

        col.update_many(query['query'], query['update'])

    def find_all(self, col_name: CollectionName):
        return self._client.db_stego[col_name.name].find({})

    def find_one_by(self, query: dict[str, any], project=None):
        self.validate_find(query)
        if project is None:
            project = {}
        res = list(self._client.db_stego[query['collection'].name].find(query['query'], project))

        return res[0] if len(res) >= 0 else None

    def find_all_by(self, query: dict[str, any], project=None):
        self.validate_find(query)
        if project is None:
            project = {}
        return self._client.db_stego[query['collection'].name].find(query['query'], project)
