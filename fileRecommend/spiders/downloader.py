from spiders.middleware import DownloaderMiddlewareManager

#下载器
class Downloader(object):
    '''下载器'''
    def __init__(self,crawler):
        # 拿到settings对象
        self.settings = crawler.settings
        # 从配置中获取设置的并发数
        self.total_concurrency = self.settings.getint('CONCURRENT_REQUESTS')
        # 同一域名并发数
        self.domain_concurrency = self.settings.getint('CONCURRENT_REQUESTS_PER_DOMAIN')
        # 同一IP并发数
        self.ip_concurrency = self.settings.getint('CONCURRENT_REQUESTS_PER_IP')
        # 随机延迟下载时间
        self.randomize_delay = self.settings.getbool('RANDOMIZE_DOWNLOAD_DELAY')
        # 初始化中间件
        self.middleware = DownloaderMiddlewareManager.from_crawler(crawler) #即便继承了父类，cls代表的还是自己



#下载处理器
class DownloadHandler(object):
    '''下载处理器'''
    def __init__(self,crawler):
        self._crawler = crawler