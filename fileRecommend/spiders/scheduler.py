from spiders import load_object
#调度器
class Scheduler(object):
    '''
    任务调度器：使用队列
    '''
    def __init__(self,dupefilter,mqclass=None):
        # 指纹过滤器
        self.df = dupefilter
        # 内存任务队列
        self.mqclass = mqclass

    @classmethod
    def from_crawler(cls,crawler):
        settings = crawler.settings
        # 从配置文件中获取指纹过滤器
        dupefilter_cls = load_object(settings['DUPEFILTER_CLASS'])
        # 实例化
        dupefilter = dupefilter_cls.from_settings(settings)
        # 获取内存任务队列类
        mqclass = load_object(settings['SCHEDULER_MEMORY_QUEUE'])
        return cls(dupefilter,mqclass)