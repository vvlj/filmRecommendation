#各个基本组件
DOWNLOAD_HANDLERS_BASE ='spiders.downloader.DownloadHandler'
DOWNLOADER_MIDDLEWARES_BASE = []
DOWNLOADER_MIDDLEWARES = []
ITEM_PIPELINES_BASE = ''
SPIDER_MIDDLEWARES_BASE = []


#类
SPIDER_MANAGER_CLASS = 'spiders.spider.Spider'  #简化了管理器
SCHEDULER = 'spiders.scheduler.Scheduler'
DOWNLOADER =  'spiders.downloader.Downloader'
ITEM_PROCESSOR ='spiders.pipelines.ItemPipelineManager' #pipeline处理器

#列表
SPIDER_MODULES =['a','b','c']
ITEM_PIPELINES = []


#int
REACTOR_THREADPOOL_MAXSIZE = 10
DNSCACHE_SIZE = -1
CONCURRENT_REQUESTS = -1    # 并发数
CONCURRENT_REQUESTS_PER_DOMAIN = -1 #同一域名的并发数
CONCURRENT_REQUESTS_PER_IP = -1 #同一ip的并发数
CONCURRENT_ITEMS = -1   #同时处理输出的任务个数
#bool
DNSCACHE_ENABLED = False    #dns缓存
RANDOMIZE_DOWNLOAD_DELAY = False #随机延迟下载


