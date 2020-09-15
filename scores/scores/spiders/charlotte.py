import scrapy
import sys

from scores.items import ScoresItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class ScoreSpider(scrapy.Spider):
    name = "charlotte"

    def start_requests(self):
        '''
            TODO: How to handle different http return codes
        '''
        queryUrl = "http://www.ufcstats.com/statistics/fighters/search?query=" + self.last.strip().lower()
        urls = [queryUrl]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_fighters, errback=self.errback_general)


    def errback_general(self, failure):
        self.logger.error(repr(failure))
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on {response_url}'.format(response_url=response.url))

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on {request_url}'.format(request_url=request.url))

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on {request_url}'.format(request_url=request.url))

    def parse_fighters(self, response):
        '''
            Find fighter
        '''
        xpathStr = '//tbody/tr/td/a[contains(translate(text(), "ABCEDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnoqrstuvwxyz"), "{firstName}")]/@href'
        href_list = response.xpath(xpathStr.format(firstName=self.first.strip().lower())).extract()
        if len(href_list) == 0:
            self.logger.debug("Found no match")
            return
        elif len(href_list) == 1:
            self.logger.debug("Found 1 match")
            yield response.follow(href_list[0], callback=self.parse_stats, errback=self.errback_general)
        elif len(href_list) > 1:
            self.logger.debug("Found multiple matches")
            self.logger.warning("Haven't implemented multiple matches")
            return

    def parse_stats(self, response):
        '''
            Extract record
            TODO: Extract different record items
        '''
        item = ScoresItem()
        xpathStr = '//*[@class="b-content__title-record"]/text()'
        record_list = response.xpath(xpathStr).extract()
        if(len(record_list) == 1):
            item['record'] = record_list[0].strip()
        else:
            self.logger.warning("Haven't implemented multiple list record")
            return
        return item        
