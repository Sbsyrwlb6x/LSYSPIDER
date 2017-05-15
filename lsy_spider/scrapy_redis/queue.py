from scrapy.utils.reqser import request_to_dict, request_from_dict
from scrapy.http import Request

try:
    import cPickle as pickle
except ImportError:
    import pickle


class Base(object):
    """Per-spider queue/stack base class"""

    def __init__(self, server, spider, key, queue_name):
        """Initialize per-spider redis queue.

        Parameters:
            server -- redis connection
            spider -- spider instance
            key -- key for this queue (e.g. "%(spider)s:queue")
        """
        self.server = server
        self.spider = spider
        self.key = key % {'spider': queue_name}

    def _encode_request(self, request):
        """Encode a request object"""
        return pickle.dumps(request_to_dict(request, self.spider), protocol=-1)

    def _decode_request(self, encoded_request):
        """Decode an request previously encoded"""
        return request_from_dict(pickle.loads(encoded_request), self.spider)

    def __len__(self):
        """Return the length of the queue"""
        raise NotImplementedError

    def push(self, request):
        """Push a request"""
        raise NotImplementedError

    def pop(self, timeout=0):
        """Pop a request"""
        raise NotImplementedError

    def clear(self):
        """Clear queue/stack"""
        self.server.delete(self.key)


class SpiderQueue(Base):
    """Per-spider FIFO queue"""

    def __len__(self):
        """Return the length of the queue"""
        return self.server.llen(self.key)

    def push(self, request):
        """Push a request"""
        self.server.lpush(self.key, self._encode_request(request))

    def pop(self, timeout=0):
        """Pop a request"""
        if timeout > 0:
            data = self.server.brpop(self.key, timeout)
            if isinstance(data, tuple):
                data = data[1]
        else:
            data = self.server.rpop(self.key)
        if data:
            return self._decode_request(data)


class SpiderPriorityQueue(Base):
    """Per-spider priority queue abstraction using redis' sorted set"""

    def __len__(self):
        """Return the length of the queue"""
        return self.server.zcard(self.key)

    def push(self, request):
        """Push a request"""
        data = self._encode_request(request)
        pairs = {data: -request.priority}
        self.server.zadd(self.key, **pairs)

    def pop(self, timeout=0):
        """
        Pop a request
        timeout not support in this queue class
        """
        # use atomic range/remove using multi/exec
        pipe = self.server.pipeline()
        pipe.multi()
        pipe.zrange(self.key, 0, 0).zremrangebyrank(self.key, 0, 0)
        results, count = pipe.execute()
        if results:
            return self._decode_request(results[0])

class NewQueue(Base):
    def __len__(self):
        """返回队列长度"""
        return self.server.zcard(self.key)

    def push(self, request):
        """头插 入队"""
        self.server.lpush(self.key, request.url[15:])

    def pop(self, timeout=0):
        """尾出 出队"""
        if timeout > 0:
            url = self.server.brpop(self.key, timeout=timeout)
            if isinstance(url, tuple):
                url = url[1]
        else:
            url = self.server.rpop(self.key)
        if url:
            try:
                if "/follow" in url or "/fans" in url:
                    cb = getattr(self.spider, "parse_relationship")
                elif "/profile" in url:
                    cb = getattr(self.spider, "parse_tweets")
                elif "/info" in url:
                    cb = getattr(self.spider, "parse_information")
                else:
                    raise ValueError("方法未找到: %s( URL:%s )" % (self.spider, url))
                return Request(url="http://weibo.cn%s" % url, callback=cb)
            except AttributeError:
                raise ValueError("方法未找到: %s( URL:%s )" % (self.spider, url))

__all__ = ['SpiderQueue', 'SpiderPriorityQueue']
