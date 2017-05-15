import settings
import redis

if __name__ == '__main__':
    try:
        rconn = redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT, settings.REDIS_DB)
    except Exception:
        rconn = redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT)

    try:
        rconn_filter = redis.Redis(settings.FILTER_HOST, settings.FILTER_PORT, settings.FILTER_DB)
    except Exception:
        try:
            rconn_filter = redis.Redis(settings.FILTER_HOST, settings.FILTER_PORT)
        except Exception:
            rconn_filter = None

    if rconn:
        if 'lsy_spider:requests' in rconn.keys():
            rconn.delete('lsy_spider:requests')

    if rconn_filter:
        if 'lsy_spider:dupefilter0' in rconn.keys():
            rconn.delete('lsy_spider:dupefilter0')
        if 'lsy_spider:dupefilter1' in rconn.keys():
            rconn.delete('lsy_spider:dupefilter1')

    print 'Finish!'
