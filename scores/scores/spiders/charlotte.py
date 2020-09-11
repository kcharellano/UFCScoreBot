import scrapy
from scores.items import ScoresItem


class ScoreSpider(scrapy.Spider):
    name = "charlotte"

    def start_requests(self):
        queryUrl = "http://www.ufcstats.com/statistics/fighters/search?query=" + self.last 
        urls = [queryUrl]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        '''
            Find fighter
        '''
        xpathStr = '//tbody/tr/td/a[text()="%s"]/@href' % self.first
        nextPage = response.xpath(xpathStr).extract()[0]
        if nextPage is not None:
            yield response.follow(nextPage, callback=self.afterParse)

    def afterParse(self, response):
        '''
            Extract record
        '''
        item = ScoresItem()
        xpathStr = '//*[@class="b-content__title-record"]/text()'
        item['record'] = response.xpath(xpathStr).extract()
        return item        
