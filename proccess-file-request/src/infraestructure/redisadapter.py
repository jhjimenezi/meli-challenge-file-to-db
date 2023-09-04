import redis

class RedisAdapter:
    redis = None

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        pool = redis.ConnectionPool(host=self.host, port=self.port, db=0)
        self.redis = redis.Redis(connection_pool=pool)
    
    def set(self, key, value):
        self.redis.set(key, value)        
    
    def get(self, key):
        return self.redis.get(key)