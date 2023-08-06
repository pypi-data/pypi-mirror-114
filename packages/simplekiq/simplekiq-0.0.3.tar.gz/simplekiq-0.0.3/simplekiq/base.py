from .constants import Constants
import json
import redis


class KiqQueue:
    def __init__(self, addr, name, create=True):
        if not name:
            raise Exception("Queue name should be supported")

        self.addr = addr
        self.conn = self.connect_to_redis(addr)
        self._name = name
        self._queue_name = Constants.QUEUE_TPL.format(name)
        if create:
            self.conn.sadd(Constants.QUEUES_NAME, self._name)

    def connect_to_redis(self, addr):
        return redis.from_url(f"redis://{addr}/")
    
    @property
    def name(self):
        return self._name

    @property
    def queue_name(self):
        return self._queue_name

    def enqueue(self, event):
        try:
            self.conn.rpush(self.queue_name, json.dumps(event))
            return True
        except redis.exceptions.ConnectionError as e:
            self.conn = self.connect_to_redis(self.addr)
            return False
            
        
    def dequeue(self, wait=True):
        try:
            if wait:
                v = self.conn.blpop(self.queue_name)[1]
            else:
                v = self.conn.lpop(self.queue_name)

            if v:
                return json.loads(v.decode('utf-8'))
            else:
                return None
        except redis.exceptions.ConnectionError as e:
            self.conn = self.connect_to_redis(self.addr)
            return None
