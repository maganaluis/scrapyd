from zope.interface import implementer

from scrapyd.interfaces import ISpiderQueue
from scrapyd.sqlite import JsonSqlitePriorityQueue
from .mongodb import MongoDBPriorityQueue


#@implementer(ISpiderQueue)
class SqliteSpiderQueue(object):

    def __init__(self, database=None, table='spider_queue'):
        self.q = JsonSqlitePriorityQueue(database, table)

    def add(self, name, priority=0.0, **spider_args):
        d = spider_args.copy()
        d['name'] = name
        self.q.put(d, priority=priority)

    def pop(self):
        return self.q.pop()

    def count(self):
        return len(self.q)

    def list(self):
        return [x[0] for x in self.q]

    def remove(self, func):
        return self.q.remove(func)

    def clear(self):
        self.q.clear()

@implementer(ISpiderQueue)
class MongoDBSpiderQueue(object):
    class __MongoDBSpiderQueue(SqliteSpiderQueue):
        def __init__(self, config, collection):
            self.q = MongoDBPriorityQueue(config, collection)
    instance = None
    def __new__(cls, config, collection): # __new__ always a classmethod
        if not MongoDBSpiderQueue.instance:
            MongoDBSpiderQueue.instance = MongoDBSpiderQueue.__MongoDBSpiderQueue(config, collection)
        return MongoDBSpiderQueue.instance
    def __getattr__(self, name):
        return getattr(self.instance, name)
    def __setattr__(self, name):
        return setattr(self.instance, name)
