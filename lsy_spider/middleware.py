# encoding=utf-8
import os
import random
import redis
import json
import logging
from lsy_spider.weiboID import getFileOrderByUpdate
from lsy_spider.weiboID import usefile
K=getFileOrderByUpdate("C:\\lsy_spider\\lsy_spider\\log")
from user_agents import agents
from cookies import initCookie, updateCookie, removeCookie
from scrapy.exceptions import IgnoreRequest
from scrapy.utils.response import response_status_message
from scrapy.downloadermiddlewares.retry import RetryMiddleware

logger = logging.getLogger(__name__)
handler=logging.FileHandler(K)
logger.addHandler(handler)
# class ProxyMiddleware(object):
#     def process_request(self, request, spider):
#         p=random.choice(proxys)
#         request.meta['proxy'] = p


#随机切user-agent 防封
class UserAgentMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent

# 维护cookie池
class CookiesMiddleware(RetryMiddleware):
    # 重载父类 调用init
    def __init__(self, settings, crawler):
        RetryMiddleware.__init__(self, settings)
        self.rconn = settings.get("RCONN", redis.Redis(crawler.settings.get('REDIS_HOST', 'localhsot'), crawler.settings.get('REDIS_PORT', 6379)))
        #往redis中添加cookie
        # initCookie(self.rconn, crawler.spider.name)
    #http://scrapy-chs.readthedocs.io/zh_CN/latest/topics/settings.html#how-to-access-settings
    @classmethod
    # 类方法 from_crawler 将它传递给扩展(extensions)
    # 该对象提供对所有Scrapy核心组件的访问， 也是扩展访问Scrapy核心组件和挂载功能到Scrapy的唯一途径
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)
    # http://scrapy-chs.readthedocs.io/zh_CN/latest/topics/downloader-middleware.html?highlight=process_request
    def process_request(self, request, spider):
        # 从redis中获取所有keys,list中全是字符串类型
        redisKeys = self.rconn.keys()
        while len(redisKeys) > 0:
            elem = random.choice(redisKeys)
            if "lsy_spider:Cookies" in elem:
                cookie = json.loads(self.rconn.get(elem))
                request.cookies = cookie
                request.meta["accountText"] = elem.split("Cookies:")[-1]
                if not cookie:
                    redisKeys.remove(elem)
                    strs=u"删除了一个空Cookie..."
                    usefile(strs)
                    print u"删除了一个空Cookie..."
                break
            else:
                redisKeys.remove(elem)
                strs = u"删除了一个空Cookie......"
                usefile(strs)
                print u"删除了一个空Cookie......"

    def process_response(self, request, response, spider):
        # 根据 HTTP标准 ，返回值为200-300之间的值为成功的resonse
        if response.status in [300, 301, 302, 303]:
            try:
                redirect_url = response.headers["location"]
                if "login.weibo" in redirect_url or "login.sina" in redirect_url:  # Cookie失效
                    strs=u"发现一个Cookie失效，需要更新........."+'\n'
                    print strs
                    logger.warning(u"发现一个Cookie失效，需要更新........."+'\n')
                    updateCookie(request.meta['accountText'], self.rconn, spider.name)
                elif "weibo.cn/security" in redirect_url:  # 账号被限
                    strs=u"发现一个账号被限制，需要删除........."+'\n'
                    print strs
                    logger.warning(u"发现一个账号被限制，需要删除.........")
                    removeCookie(request.meta["accountText"], self.rconn, spider.name)
                elif "weibo.cn/pub" in redirect_url:
                    strs=u"重定向'http://weibo.cn/pub'!( Account:%s )" % request.meta["accountText"].split("--")[0]+'\n'
                    print strs
                    logger.warning(
                        u"重定向'http://weibo.cn/pub'!( Account:%s )" % request.meta["accountText"].split("--")[0])
                reason = response_status_message(response.status)
                return self._retry(request, reason, spider) or response  # 重试
            except Exception, e:
                raise IgnoreRequest
        elif response.status in [403, 414]:
            strs=u"%s! 系统停止运行........." % response.status+'\n'
            print strs
            logger.error(u"%s! 系统停止运行........." % response.status)

            content=input(u"请切换代理:")
            logger.error(u"请切换代理:"+'\n')

            if content=="goon":
                return response
            else:
                os.system("pause")
            # os.system("pause")
        else:
            return response
