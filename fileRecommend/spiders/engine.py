from spiders import load_object
from spiders.scraper import Scraper
from twisted.internet import reactor,defer

import scrapy.pipelines

class ExecutionEngine(object):
    def __init__(self, crawler, spider_closed_callback):
        # crawler、设置、信号、调度器、下载器、scraper
        self.crawler = crawler
        self.settings = crawler.settings
        #self.signals = crawler.signals
        self.spider = None
        self.running = False
        self.paused = False
        self.scheduler_cls = load_object(self.settings.get('SCHEDULER'))
        downloader_cls = load_object(self.settings.get('DOWNLOADER'))
        self.downloader = downloader_cls(crawler)

        self.scraper = Scraper(crawler)
        self._spider_closed_callback = spider_closed_callback


    def close(self):
        if self.running:
            # Will also close spiders and downloader
            return self.stop()
        elif self.open_spiders:
            # Will also close downloader
            return self._close_all_spiders()
        else:
            return defer.succeed(self.downloader.close())

    def stop(self):
        pass

    @property
    def open_spiders(self):
        return [self.spider] if self.spider else []

    def _close_all_spiders(self):
        dfds = [self.close_spider(s, reason='shutdown') for s in self.open_spiders]
        dlist = defer.DeferredList(dfds)
        return dlist

    def close_spider(self, spider, reason='cancelled'):
        """Close (cancel) spider and clear all its outstanding requests"""

        dfd.addBoth(lambda _: self.downloader.close())
        dfd.addErrback(log_failure('Downloader close failure'))

        dfd.addBoth(lambda _: self.scraper.close_spider(spider))
        dfd.addErrback(log_failure('Scraper close failure'))

        dfd.addBoth(lambda _: slot.scheduler.close(reason))
        dfd.addErrback(log_failure('Scheduler close failure'))

        dfd.addBoth(lambda _: self.signals.send_catch_log_deferred(
            signal=signals.spider_closed, spider=spider, reason=reason))
        dfd.addErrback(log_failure('Error while sending spider_close signal'))

        dfd.addBoth(lambda _: self.crawler.stats.close_spider(spider, reason=reason))
        dfd.addErrback(log_failure('Stats close failure'))

        dfd.addBoth(lambda _: logger.info("Spider closed (%(reason)s)",
                                          {'reason': reason},
                                          extra={'spider': spider}))

        dfd.addBoth(lambda _: setattr(self, 'slot', None))
        dfd.addErrback(log_failure('Error while unassigning slot'))

        dfd.addBoth(lambda _: setattr(self, 'spider', None))
        dfd.addErrback(log_failure('Error while unassigning spider'))

        dfd.addBoth(lambda _: self._spider_closed_callback(spider))

        return dfd