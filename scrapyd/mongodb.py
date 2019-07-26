import json
import pymongo
from configparser import NoOptionError

class JobItem(object):
    def __init__(self, item):
        self.project = item['project']
        self.spider = item['spider']
        self.job = item['id']
        self.pid = item['pid']
        self.start_time = item['start_time']
        self.end_time = item['end_time']


class MongoConnector(object):
    def __init__(self, config, collection):
        database_name = config.get('mongodb_name', 'scrapyd_mongodb')
        database_host = config.get('mongodb_host', 'localhost')
        database_port = config.getint('mongodb_port', 27017)
        database_user = self.get_optional_config(config, 'mongodb_user')
        database_pwd = self.get_optional_config(config, 'mongodb_pass')
        if database_user and database_pwd:
            conn_str = (
                'mongodb://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'
            ).format(
                db_user=database_user,
                db_pwd=database_pwd,
                db_host=database_host,
                db_port=database_port,
                db_name=database_name,
            )
            self.conn = pymongo.MongoClient(conn_str)
        else:
            self.conn = pymongo.MongoClient(
                host=database_host,
                port=database_port,
            )

        self.collection = self.conn.get_database(database_name)[collection]

    @staticmethod
    def get_optional_config(config, name):
        try:
            return config.get(name).replace('\'', '').replace('"', '')
        except NoOptionError:
            return None

class MongoDBJobs(MongoConnector):
    def __init__(self, config, collection):
        super().__init__(config, collection)
        self.collection.create_index("id", unique=True)

    def insert(self, item):
        result = self.collection.insert_one({
            "project": item.project,
            "spider": item.spider,
            "id": item.job,
            "pid": item.pid,
            "start_time": item.start_time,
            "end_time": item.end_time
        })
        return result

    def update(self, item):
        result = self.collection.update_one({'id': item.job},
        {'$set': {
            "project": item.project,
            "spider": item.spider,
            "id": item.job,
            "pid": item.pid,
            "start_time": item.start_time,
            "end_time": item.end_time
        }}, upsert=True)
        return result

    def remove(self, item):
        result = self.collection.delete_one({'id': item.job})

    def clear(self):
        self.collection.drop()

    def __len__(self):
        return self.collection.count()

    def get_jobs_runing(self):
        queryset = self.collection.find({'end_time': None}).sort([
            ('start_time', pymongo.DESCENDING),
        ])
        return iter([JobItem(q) for q in queryset])

    def get_jobs_completed(self):
        queryset = self.collection.find({'end_time': {'$ne': None}}).sort([
            ('start_time', pymongo.DESCENDING),
        ])
        return iter([JobItem(q) for q in queryset])

    def encode(self, obj):
        return json.dumps(obj)

    def decode(self, text):
        return json.loads(text)
