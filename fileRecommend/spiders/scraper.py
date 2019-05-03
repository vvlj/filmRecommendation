from spiders.middleware import SpiderMiddlewareManager
from spiders import load_object

class Scraper(object):
    def __init__(self, crawler):
        # 实例化爬虫中间件管理器
        self.spidermw = SpiderMiddlewareManager.from_crawler(crawler)
        # 从配置文件中加载Pipeline处理器类
        itemproc_cls = load_object(crawler.settings.get('ITEM_PROCESSOR'))

        # 实例化Pipeline处理器
        self.itemproc = itemproc_cls.from_crawler(crawler)
        # 从配置文件中获取同时处理输出的任务个数
        self.concurrent_items = crawler.settings.getint('CONCURRENT_ITEMS')
        self.crawler = crawler