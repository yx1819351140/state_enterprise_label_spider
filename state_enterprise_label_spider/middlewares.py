# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import redis
import random
from twisted.internet.error import TCPTimedOutError


class StateEnterpriseLabelSpiderSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class StateEnterpriseLabelSpiderDownloaderMiddleware:
    def __init__(self, proxy, proxies_list):
        self.proxy = proxy
        self.proxies_list = proxies_list

    @classmethod
    def from_crawler(cls, crawler):
        # 从Scrapy设置中读取Redis配置
        host = crawler.settings.get('REDIS_HOST')
        port = crawler.settings.get('REDIS_PORT')
        db = crawler.settings.get('REDIS_DB')
        key = crawler.settings.get('REDIS_KEY')

        # 连接到Redis并获取代理列表
        pool = redis.ConnectionPool(host=host, port=port, db=db, decode_responses=True)
        r = redis.Redis(connection_pool=pool)
        proxies_list = r.zrange(key, 0, -1)
        proxy = 'http://' + random.choice(proxies_list)

        s = cls(proxy, proxies_list)
        s.proxies_list = proxies_list
        s.redis = r
        s.redis_key = key

        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # 设置代理
        if 'proxy' not in request.meta:
            request.meta['proxy'] = self.proxy

        # 初始化失败计数器
        if 'retry_count' not in request.meta:
            request.meta['retry_count'] = 0

        return None

    def process_response(self, request, response, spider):
        # 返回正常的response
        return response

    def process_exception(self, request, exception, spider):

        if isinstance(exception, (TimeoutError, TCPTimedOutError)):
            spider.logger.info(f"Timeout error for {request.url}, switching proxy")
            new_proxy = 'http://' + random.choice(self.proxies_list)
            spider.logger.info(f"Changing proxy from {self.proxy} to {new_proxy}")
            request.meta['proxy'] = new_proxy
            request.meta['retry_count'] = 0  # 重置失败计数器
            return request  # 返回重新处理的请求

        # 增加失败次数
        request.meta['retry_count'] += 1

        # 如果失败次数达到5次，更换代理并重新发送请求
        if request.meta['retry_count'] >= 5:
            spider.logger.info(f"Retrying {request.url} with a new proxy due to {exception}")
            new_proxy = 'http://' + random.choice(self.proxies_list)
            self.proxy = new_proxy
            spider.logger.info(f"Changing proxy from {self.proxy} to {new_proxy}")
            request.meta['proxy'] = new_proxy
            request.meta['retry_count'] = 0  # 重置失败计数器
            return request  # 返回重新处理的请求

        return None

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
