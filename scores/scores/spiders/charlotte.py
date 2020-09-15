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
            TODO: What if queryUrl leads to empty fighter table?
            TODO: Multiple fighters with same name
        '''
        xpathStr = '//tbody/tr/td/a[contains(translate(text(), "ABCEDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnoqrstuvwxyz"), "{firstName}")]/@href'
        nextPage = response.xpath(xpathStr.format(firstName=self.first.strip().lower())).extract()[0]
        if nextPage is not None:
            yield response.follow(nextPage, callback=self.parse_stats, errback=errback_general)

    def parse_stats(self, response):
        '''
            Extract record
        '''
        item = ScoresItem()
        xpathStr = '//*[@class="b-content__title-record"]/text()'
        item['record'] = response.xpath(xpathStr).extract()
        return item        
