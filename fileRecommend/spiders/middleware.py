from collections import defaultdict
from spiders import load_object
import scrapy.settings
class MiddlewareManager(object):
    '''中间件基类'''
    def __init__(self,*middlewares):
        self.middlewares = middlewares
        # 定义中间件方法
        self.methods = defaultdict(list)
        for mw in middlewares:
            self._add_middleware(mw)

    def _add_middleware(self, mw):
        # 默认定义的，子类可覆盖
        # 如果中间件类有定义open_spider,则加入到methods
        if hasattr(mw, 'open_spider'):
            self.methods['open_spider'].append(mw.open_spider)
        # 如果中间件类有定义close_spider,则加入到methods
        # methods就是一串中间件的方法链，后期会依次调用
        if hasattr(mw, 'close_spider'):
            self.methods['close_spider'].insert(0, mw.close_spider)

    @classmethod
    def from_crawler(cls, crawler):     #被继承
        return cls.from_settings(crawler.settings, crawler)

    @classmethod
    def _get_mwlist_from_settings(cls, settings):
        raise NotImplementedError   #未实现的方法，该方法要在子类实现


    @classmethod
    def from_settings(cls, settings, crawler=None):
        mwlist = cls._get_mwlist_from_settings(settings)
        middlewares = []
        enabled = []
        for clspath in mwlist:
            try:
                mwcls = load_object(clspath)
                #初始化中间件的三种方式
                if crawler and hasattr(mwcls, 'from_crawler'):
                    mw = mwcls.from_crawler(crawler)
                elif hasattr(mwcls, 'from_settings'):
                    mw = mwcls.from_settings(settings)
                else:
                    mw = mwcls()
                middlewares.append(mw)
                enabled.append(clspath)
            except:
                pass #说明丢失配置了

        return cls(*middlewares)

    def _process_chain(self,a,b,c):pass

class DownloaderMiddlewareManager(MiddlewareManager):
    """下载中间件管理器"""
    def _add_middleware(self, mw):
        # 处理中间件请求、响应、异常
        if hasattr(mw, 'process_request'):
            self.methods['process_request'].append(mw.process_request)
        if hasattr(mw, 'process_response'):
            self.methods['process_response'].insert(0, mw.process_response)
        if hasattr(mw, 'process_exception'):
            self.methods['process_exception'].insert(0, mw.process_exception)

    @classmethod
    def _get_mwlist_from_settings(cls, settings):
        # 从配置文件DOWNLOADER_MIDDLEWARES_BASE和DOWNLOADER_MIDDLEWARES获得所有下载器中间件
        return settings.getwithbase('DOWNLOADER_MIDDLEWARES')

class SpiderMiddlewareManager(MiddlewareManager):
    """爬虫中间件管理器"""
    def _add_middleware(self, mw):
        super(SpiderMiddlewareManager, self)._add_middleware(mw)    #继承
        # 处理输入、输出、异常、初始请求
        if hasattr(mw, 'process_spider_input'):
            self.methods['process_spider_input'].append(mw.process_spider_input)
        if hasattr(mw, 'process_spider_output'):
            self.methods['process_spider_output'].insert(0, mw.process_spider_output)
        if hasattr(mw, 'process_spider_exception'):
            self.methods['process_spider_exception'].insert(0, mw.process_spider_exception)
        if hasattr(mw, 'process_start_requests'):
            self.methods['process_start_requests'].insert(0, mw.process_start_requests)

    @classmethod
    def _get_mwlist_from_settings(cls, settings):
        return settings.getwithbase('SPIDER_MIDDLEWARES_BASE')

class ItemPipelineManager(MiddlewareManager):

    component_name = 'item pipeline'

    @classmethod
    def _get_mwlist_from_settings(cls, settings):
        return settings.getlist('ITEM_PIPELINES')

    def _add_middleware(self, pipe):
        super(ItemPipelineManager, self)._add_middleware(pipe)
        if hasattr(pipe, 'process_item'):
            self.methods['process_item'].append(pipe.process_item)