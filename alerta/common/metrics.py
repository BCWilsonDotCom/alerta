
import time
import pymongo

from alerta.common import settings

conn = pymongo.Connection(
    host=getattr(settings, 'mongo_host', 'localhost'),
    port=getattr(settings, 'mongo_port', 27017),
    network_timeout=1
)

db = conn[getattr(settings, 'mongo_database', 'monitoring')]

username = getattr(settings, 'mongo_username', 'alerta')
password = getattr(settings, 'mongo_password', None)

if username and password:
    db.authenticate(username, password)


class Gauge(object):

    def __init__(self, group, name, title=None, description=None):

        self.group = group
        self.name = name
        self.title = title
        self.description = description

    def set(self, value):

        db.metrics.update(
            {
                "group": self.group,
                "name": self.name
            },
            {
                "group": self.group,
                "name": self.name,
                "title": self.title,
                "description": self.description,
                "value": value,
                "type": "gauge"
            },
            True
        )

    @classmethod
    def get_gauges(cls):

        return list(db.metrics.find({"type": "gauge"}, {"_id": 0}))


class Counter(object):

    def __init__(self, group, name, title=None, description=None):

        self.group = group
        self.name = name
        self.title = title
        self.description = description

    def inc(self):

        db.metrics.update(
            {
                "group": self.group,
                "name": self.name
            },
            {
                '$set': {
                    "group": self.group,
                    "name": self.name,
                    "title": self.title,
                    "description": self.description,
                    "type": "counter"
                },
                '$inc': {"count": 1}
            },
            True
        )

    @classmethod
    def get_counters(cls):

        return list(db.metrics.find({"type": "counter"}, {"_id": 0}))


class Timer(object):

    def __init__(self, group, name, title=None, description=None):

        self.group = group
        self.name = name
        self.title = title
        self.description = description

        self.start = None

    @staticmethod
    def _time_in_millis():

        return int(round(time.time() * 1000))

    def start_timer(self):

        return self._time_in_millis()

    def stop_timer(self, start):

        db.metrics.update(
            {
                "group": self.group,
                "name": self.name
            },
            {
                '$set': {
                    "group": self.group,
                    "name": self.name,
                    "title": self.title,
                    "description": self.description,
                    "type": "timer"
                },
                '$inc': {"count": 1, "totalTime": self._time_in_millis() - start}
            },
            True
        )

    @classmethod
    def get_timers(cls):

        return list(db.metrics.find({"type": "timer"}, {"_id": 0}))
