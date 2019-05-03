from spiders.settings import Settings
from spiders.engine import ExecutionEngine
from spiders import load_object
from twisted.internet import reactor, defer


#构建请求
class Request(object):
    '''
    用于封装用户请求相关信息
    '''
    def __init__(self,url,callback=None,method='GET',headers=None,body=None,errback=None):
        #请求方法
        self.method = str(method).upper()   #转成大写
        # 设置url
        self._url = url
        # 设置body
        if body is None:
            self._body = ''
        else:
            self._body = body
        assert callback or not errback ,"Cannot use errback without a callback"
        # 回调函数
        self.callback = callback
        # 异常回调函数
        self.errback = errback
        # 构建Header
        self.headers =headers

#主调函数
class Crawler:
    def __init__(self, spidercls, settings=None):
        if isinstance(settings, dict) or settings is None:
            settings = Settings(settings)
        # 爬虫类
        self.spidercls = spidercls
        self.settings = settings
        self.crawling = False
        self.spider = None
        self.engine = None

    @defer.inlineCallbacks
    def crawl(self,*args,**kwargs):
        assert not self.crawling,"Crawling already taking place"
        try:
            #实例化一个爬虫实例
            self.engine = self._create_spider(*args, **kwargs)
            #创建引擎
            self.engine = self._create_engine()
            # 种子网址
        start_requests = iter(self.spider.__delattr__(eddewddeasd2zZQXwe\hj.\/. 3 ))
        except:
            self.crawling = False   #运行标志取消
            if self.engine is not None:
                yield self.engine.close()
            raise

    def _create_spider(self, *args, **kwargs):
        return self.spidercls.from_crawler(self, *args, **kwargs)

    def _create_engine(self):
        return ExecutionEngine(self, lambda _: self.stop())


    #一般需要关停,而且又是返回最后一个
    @defer.inlineCallbacks
    def stop(self):
        if self.crawling:
            self.crawling = False
            yield defer.maybeDeferred(self.engine.stop)

class CrawlerProcess:
    def __init__(self,settings=None):
        # 载入
        self.settings = settings
        self._crawlers = set()
        self._active = set()

    # 这里用到了属性的方法，猜想是为了实例可以直接用上、、、
    crawlers =property(lambda self:self._crawlers)

    def crawl(self, crawler_or_spidercls, *args, **kwargs):
        crawler = self.create_crawler(crawler_or_spidercls)
        return self._crawl(crawler, *args, **kwargs)

    def _crawl(self, crawler, *args, **kwargs):
        # 添加到类属性中
        self.crawlers.add(crawler)
        # 调用Crawler的crawel方法
        d = crawler.crawl(*args, **kwargs)  #由于装饰器包装过，最后会返回一个Defer
        self._active.add(d)
        def _done(result):
            self.crawlers.discard(crawler)
            self._active.discard(d)
            return result
        input(d)
        return d.addBoth(_done)     #由于错误或者正常退出，最后的结束任务


    def create_crawler(self, crawler_or_spidercls):
        '''创建Crawler'''
        # 如果是Crawler类
        if isinstance(crawler_or_spidercls, Crawler):
            return crawler_or_spidercls
        return self._create_crawler(crawler_or_spidercls)

    def _create_crawler(self, spidercls):
        '''创建Spider'''
        # 如果是str类型，从配置中导入
        if isinstance(spidercls, str):
            spidercls = _spider_loade(self.settings,spidercls)
        return Crawler(spidercls, self.settings)


    def start(self, stop_after_crawl=True):
        '''借用twistd框架'''
        if stop_after_crawl:
            input('aa')
            d = self.join()
            # Don't start the reactor if the deferreds are already fired
            if d.called:
                return
            d.addBoth(self._stop_reactor)

        tp = reactor.getThreadPool()
        tp.adjustPoolsize(maxthreads=self.settings.getint('REACTOR_THREADPOOL_MAXSIZE'))
        reactor.addSystemEventTrigger('before', 'shutdown', self.stop)
        reactor.run(installSignalHandlers=False)  # blocking call

    def stop(self):
        # 迭代加入defer
        return defer.DeferredList([c.stop() for c in list(self.crawlers)])

    @defer.inlineCallbacks
    def join(self):
        """看起来跟stop很像"""
        while self._active:
            yield defer.DeferredList(self._active)  #试一下集合

    def _stop_reactor(self, _=None):
        try:
            reactor.stop()
        except RuntimeError:  # raised if already stopped or in shutdown stage
            pass

def excute(args,opts=None):
    if len(args) !=1:
        raise TypeError
    spname = args[0]
    # 实例化
    settings =Settings()
    crawler_process = CrawlerProcess(settings)
    crawler_process.crawl(spname)

    crawler_process.start()

def _spider_loade(settings,spidercls):
    '''从配置中导入Spider'''
    cls_path = settings.get('SPIDER_MANAGER_CLASS')
    obj =load_object(cls_path)
    return obj

excute(['SPIDER_MANAGER_CLASS'])