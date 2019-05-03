
class Spider(object):
    '''爬虫类'''
    name = 'default'
    def __init__(self,name=None,**kwargs):
        if name is not None:
            self.name = name
        elif not getattr(self,'name',None):
            raise TypeError("%s must have a name" % type(self).__name__)
        if not hasattr(self,'start_urls'):
            # 种子url
            self.start_urls =[]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(*args, **kwargs)
        spider._set_crawler(crawler)
        return spider

    def _set_crawler(self, crawler):
        self.crawler = crawler
        self.settings = crawler.settings

    @staticmethod   #为何要关闭
    def close(spider, reason):
        closed = getattr(spider, 'closed', None)
        if callable(closed):
            return closed(reason)




