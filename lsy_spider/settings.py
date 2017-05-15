# encoding=utf-8
from lsy_spider.weiboID import getFileOrderByUpdate
K=getFileOrderByUpdate("C:\\lsy_spider\\lsy_spider\\log")
BOT_NAME = ['lsy_spider']

SPIDER_MODULES = ['lsy_spider.spiders']
NEWSPIDER_MODULE = 'lsy_spider.spiders'
DOWNLOADER_MIDDLEWARES = {
# 'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware' : 90 ,
# 'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware' : 110 ,
#     "lsy_spider.middleware.ProxyMiddleware": 1,
    "lsy_spider.middleware.UserAgentMiddleware": 401,
    "lsy_spider.middleware.CookiesMiddleware": 402,

}
ITEM_PIPELINES = {
    "lsy_spider.pipelines.MongoDBPipeline": 403,
}

SCHEDULER = 'lsy_spider.scrapy_redis.scheduler.Scheduler'
#不清除Redis队列、这样可以暂停/恢复 爬取
SCHEDULER_PERSIST = True
#使用优先级调度请求队列 （默认使用）
SCHEDULER_QUEUE_CLASS = 'lsy_spider.scrapy_redis.queue.SpiderPriorityQueue'
#可选用的其它队列
#SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.FifoQueue'
#SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.LifoQueue'
#SCHEDULER_QUEUE_CLASS = 'lsy_spider.scrapy_redis.queue.SpiderSimpleQueue'

# 种子队列的信息
# REDIE_URL = 'r-bp1968fa5d4b6f34.redis.rds.aliyuncs.com'
# REDIS_HOST = '139.129.117.12'
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
#确保所有的爬虫通过Redis去重
#DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 去重队列的信息
FILTER_URL = None
FILTER_HOST = 'localhost'
FILTER_PORT = 6379
FILTER_DB = 0

DOWNLOAD_DELAY = 0 # 间隔时间
'''
Scrapy提供5层logging级别:
CRITICAL - 严重错误(critical)
ERROR - 一般错误(regular errors)
WARNING - 警告信息(warning messages)
INFO - 一般信息(informational messages)
DEBUG - 调试信息(debugging messages)
'''
# LOG_LEVEL = 'INFO'  # 日志级别
LOG_FILE = K
CONCURRENT_REQUESTS = 16  # 默认为16
# CONCURRENT_ITEMS = 1
# CONCURRENT_REQUESTS_PER_IP = 1
REDIRECT_ENABLED = True # 允许重定向


AUTO_PROXY = {
    'download_timeout': 30,
    'test_urls': [('http://upaiyun.com', 'online'), ('http://huaban.com', '33010602001878')],
    'ban_code': [500, 502, 503, 504],
}

